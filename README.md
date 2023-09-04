# Huawei Cloud OpenStack ECS Start/Stop Function

This is a Python function designed to start or stop instances in a Huawei Cloud environment. It utilizes the OpenStack SDK to connect to your Huawei Cloud infrastructure and initiate the start/stop operation for selected servers. The function can be used within a serverless environment like HWC FGS (FunctionGraph Service).

## IMPORTANT NOTES

- This function doesn't include proper error handling for the Lambda environment. Make sure to implement proper error handling mechanisms for production use.

- The function is provided as a starting point and can be extended to suit your specific use case and error handling requirements.


## Prerequisites

1. **Huawei Cloud Credentials**: You need valid Huawei Cloud credentials including Project ID, Domain, Region, Access Key (AK), and Secret Key (SK).

2. **For Huawei Cloud**: Creation of a cloud service agency with ECS full access permission and cloud service "FunctionGraph". 

3. **Dependencies**: The function uses the `openstacksdk` library for interacting with Huawei Cloud. Make sure to have it installed using `pip install openstacksdk`, or add it to your HWC FGS Function dependencies.

## Function Overview

The function `handler(event, context)` is the main entry point and handles the Lambda event and context objects. It retrieves necessary configuration values from the context, connects to OpenStack, and starts/stops instances based on predefined white lists.

## Usage

1. **Runtime**: Python 2.7

2. **Variables**: Modify the following parameters in the code or add them as environment variables in the function if using HWC FGS:

   - `projectId`: Your Huawei Cloud region project ID.
   - `region`: The Huawei Cloud region where your instances are located (e.g., la-south-2).
   - `domain`: Huawei Cloud Domain (default value: 'myhuaweicloud.com').
   - `ak`: Your Access Key (AK).
   - `sk`: Your Secret Key (SK).
   - `whiteLists` (optional): A comma-separated list of instance names to exclude from starting/stopping.

2. **For Huawei Cloud FGS Service**: Set an agency with ECS full access permissions and increase the timeout value of the function.

3. **Response**: The function will provide a response indicating whether the servers were started/stopped successfully or if an error occurred.


## License

This code is provided under the MIT License.
