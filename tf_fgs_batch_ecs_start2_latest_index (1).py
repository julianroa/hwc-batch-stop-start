# -*- coding:utf-8 -*-

# Import necessary libraries
import json
import ssl
import time
import sys
from openstack import connection
from threading import Thread

# Disable SSL verification (not recommended for production use)
ssl._create_default_https_context = ssl._create_unverified_context

# Handler function for the AWS Lambda
def handler(event, context):
    try:
        # Extract required information from context
        projectId = context.getUserData('projectId', '').strip()
        region = context.getUserData('region', '').strip()
        domain = context.getUserData('domain', '').strip()
        ak = context.getAccessKey().strip()
        sk = context.getSecretKey().strip()
        whiteList = context.getUserData('whiteLists', '').strip().split(',')
        logger = context.getLogger()

        # Check configuration values
        if not projectId:
            raise Exception("'projectId' not configured")

        if not region:
            raise Exception("'region' not configured")

        if not domain:
            logger.info("domain not configured, use default value:myhuaweicloud.com")
            domain = 'myhuaweicloud.com'

        if not ak or not sk:
            ak = context.getUserData('ak', '').strip()
            sk = context.getUserData('sk', '').strip()
            if not ak or not sk:
                raise Exception("ak/sk empty")

        # Start ECS instances
        _start_ecs(logger, projectId, domain, region, ak, sk, whiteList)

        # Prepare and return the response
        response = {
            "statusCode": 200,
            "isBase64Encoded": False,
            "headers": {},
            "body": "Servers started successfully"
        }
    except Exception as e:
        # Handle exceptions by generating an error response
        response = {
            "statusCode": 500,
            "isBase64Encoded": False,
            "headers": {},
            "body": "An error occurred: %s" % str(e)
}

    
    return {
        "statusCode": response["statusCode"],
        "headers": response["headers"],
        "body": json.dumps(response["body"]),
        "isBase64Encoded": response["isBase64Encoded"]
    }

# Function to start ECS instances
def _start_ecs(logger, projectId, domain, region, ak, sk, startWhiteList):
    try:
        # Establish connection to OpenStack
        conn = connection.Connection(project_id=projectId, domain=domain, region=region, ak=ak, sk=sk)
        threads = []
        servers = conn.compute.servers()

        # Iterate through servers
        for server in servers:       
            if server.name in startWhiteList:
                logger.info("skip start server '%s' for being in start_white lists." % (server.name))
                continue
            if "ACTIVE" == server.status:
                logger.info("skip start server '%s' for status is active(status: %s)." % (server.name, server.status))
                continue

            # Start server using a thread
            t = Thread(target=_start_server,args=(conn, server, logger) )
            t.start()
            threads.append(t)
        
        # Check if any servers were started
        if not threads:
            logger.info("no servers to be started.")
            return

        logger.info("'%d' server(s) will be started.", len(threads))

        # Wait for all threads to finish
        for t in threads:
            t.join()    
    except Exception as e:
        logger.error("An error occurred during _start_ecs: %s", str(e))

# Function to start a server
def _start_server(conn, server, logger):
    try:
        # Start the server
        logger.info("start server '%s'..." % (server.name))
        conn.compute.start_server(server)

        cost = 0
        interval = 5
        wait = 600

        # Wait for the server to become active
        while cost < wait:
            temp = conn.compute.find_server(server.id)
            if temp and "ACTIVE" != temp.status:
                time.sleep(interval)
                cost += interval
            else:
                break

        # Check if the server started successfully
        if cost >= wait:
            logger.warn("wait for start server '%s' timeout." % (server.name))
            return 2

        logger.info("start server '%s' success." % (server.name))
        return 0
    except Exception as e:
        logger.error("An error occurred during _start_server for server '%s': %s", server.name, str(e))
