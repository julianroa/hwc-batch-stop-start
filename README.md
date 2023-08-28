# OpenStack ECS Start/Stop Function

This is a Python function designed to start or stop instances in a Huawei Cloud/OpenStack environment. It utilizes the OpenStack SDK to connect to your Huawei Cloud/OpenStack infrastructure and initiate the start/stop operation for selected servers. The function can be used within a serverless environment like HWC FGS (FunctionGraph Service).

## IMPORTANT NOTES

- This function doesn't include proper error handling for the Lambda environment. Make sure to implement proper error handling mechanisms for production use.

- The function is provided as a starting point and can be extended to suit your specific use case and error handling requirements.

- Due to potential security risks, avoid using `ssl._create_unverified_context` in production environments. Properly configure SSL certificate validation.

## Prerequisites

1. **Huawei Cloud/Openstack Credentials**: You need valid Huawei Cloud/OpenStack credentials including Project ID, Domain, Region, Access Key (AK), and Secret Key (SK).

2. **For Huawei Cloud**: Creation of a cloud service agency with ECS full access permission and cloud service "FunctionGraph".

3. **Dependencies**: The function uses the `openstacksdk` library for interacting with Huawei Cloud/OpenStack. Make sure to have it installed using `pip install openstacksdk`, or add it to your HWC FGS Function dependencies.

## Function Overview

The function `handler(event, context)` is the main entry point and handles the Lambda event and context objects. It retrieves necessary configuration values from the context, connects to OpenStack, and starts/stops instances based on predefined white lists.

## Usage

1. **Configurations**: Modify the following parameters in the code or add them as environment variables in the function if using HWC FGS:

   - `projectId`: Your Huawei Cloud/OpenStack region project ID.
   - `region`: The Huawei Cloud/OpenStack region where your instances are located.
   - `domain`: Huawei Cloud/OpenStack Domain (default value: 'myhuaweicloud.com').
   - `ak` and `sk`: Your Access Key (AK) and Secret Key (SK).
   - `whiteLists`: A comma-separated list of instance names to exclude from starting/stopping.

2. **For Huawei Cloud FGS Service**: Set an agency with ECS full access permissions and increase the timeout value of the function.

3. **Response**: The function will provide a response indicating whether the servers were started/stopped successfully or if an error occurred.


## License

This code is provided under the MIT License.
