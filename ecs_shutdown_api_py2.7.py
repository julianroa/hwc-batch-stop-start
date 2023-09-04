# -*- coding:utf-8 -*-
import json
import time,sys
from openstack import connection
from threading import Thread


# Handler function for the AWS Lambda
def handler(event, context):
    # Extract required information from context
    projectId = context.getUserData('projectId')
    domain = context.getUserData('domain')
    region = context.getUserData('region')
    ak = context.getAccessKey()
    if ak == None or ak == "":
        ak = context.getUserData('ak')
    sk = context.getSecretKey()
    if sk == None or sk == "":
        sk = context.getUserData('sk')

    # Get whitelisted servers from context
    whiteLists = context.getUserData('whiteLists')
    logger = context.getLogger()

    # Check for empty or missing configuration values
    if projectId == None or projectId == "":
        print ("projectId is empty.")
        sys.exit(1)
    if domain == None or domain == "":
        print ("domain is empty.")
        sys.exit(1)
    if region == None or region == "":
        print ("region is empty.")
        sys.exit(1)
    if ak == None or ak == "":
        print ("ak is empty.")
        sys.exit(1)
    if sk == None or sk == "":
        print ("sk is empty.")
        sys.exit(1)

    # Shutdown the ECS (Elastic Cloud Server) instances
    _shutdown_ecs(logger, projectId, domain, region, ak, sk, whiteLists)

    # Prepare and return the response
    response = {
        "statusCode": 200,
        "isBase64Encoded": False,
        "headers": {},
        "body": "Servers stopped successfully"
    }

    return {
        "statusCode": response["statusCode"],
        "headers": response["headers"],
        "body": json.dumps(response["body"]),
        "isBase64Encoded": response["isBase64Encoded"]
    }

# Function to stop a server
def _stop_server(conn, server, whites, logger):
    logger.info("try stop server %s ..." % (server.name))
    conn.compute.stop_server(server)
    total_sleep = 0
    interval = 5
    wait = 600
    while total_sleep < wait:
        temp = conn.compute.find_server(server.id)
        if temp.status and "SHUTOFF" != temp.status:
            time.sleep(interval)
            total_sleep += interval
        else:
            break
    #conn.compute.wait_for_server(server, status="SHUTOFF", interval=5, wait=600)
    if total_sleep >= wait:
        logger.warn("wait stop server %s timeout." % (server.name))
        return 2
    else:
        logger.info("stop server %s success" % (server.name))
    return 0

# Function to shut down ECS instances
def _shutdown_ecs(logger, projectId, domain, region, ak, sk, whiteLists):
    if whiteLists is None:
        whiteLists = ""
    whites = whiteLists.split(',')
    conn = connection.Connection(project_id=projectId, domain=domain, region=region, ak=ak, sk=sk) 
    threads = []
    servers = conn.compute.servers()
    for server in servers:
        try:
            if server.name in whites:
                logger.info("DO NOT shutdown %s because it is in white lists" % (server.name))
                continue
            if "ACTIVE" != server.status:
                logger.info("DO NOT shutdown %s because it is in status %s" % (server.name, server.status))
                continue
            t = Thread(target=_stop_server, args=(conn, server, whites, logger))
            t.start()
            threads.append(t)
        except Exception as e:
            logger.error("An error occurred while processing server %s: %s" % (server.name, str(e)))

    # Wait for all threads to finish
    for t in threads:
        t.join()
