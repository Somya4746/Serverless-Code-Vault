![Screenshot (660)](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/e48e25e0-53ea-404a-a43b-5fe1b84baf4d)# Serverless-Code-Vault
ServerlessCodeVault utilizes AWS Bedrock and HTTP POST API for automated code generation and storage in an AWS S3 bucket, offering a streamlined, serverless solution for efficient code management.

---

## Step-by-Step Guide

### Step 1: Initialize AWS Bedrock

1. **Login to AWS Console**: Start by logging into your AWS account.
2. **Navigate to Bedrock**: On the AWS Services dashboard, locate and click on the Bedrock service

![Screenshot (657)](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/debe1be1-6413-4aef-b9da-ed78b570902f)

3. **Region Selection**: Choose an AWS region from the top-right corner. We're using `us-east-1` for this tutorial.
4. **Access Models**: In the Bedrock dashboard, click on the **model access** tab and grant permissions.
5. **Await Approval**: Wait for AWS to grant access.
6. Make sure you have access to claude because we will be using this model.Once you have access to the models it should look something like this.
 ![Screenshot (658)](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/e4793c73-91d2-4581-b17a-3fde8fbe26f2)

### Step 2: Set Up the S3 Bucket


1. **Go to S3**: On the AWS Services dashboard, select S3.
![Screenshot (660)](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/02259001-3119-42de-a975-5353aabfa2d7)

2. **Create a New Bucket**: Click on **Create Bucket**.
3. **Naming and Region**: Name your bucket `code-gen-bucket` and select the correct region.

   
![Screenshot (661)](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/f70872ef-0e54-4a77-a99d-75507b6a097d)
4. **Bucket Settings**: Adjust settings as needed and click "Create".
![Screenshot (663)](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/4dfd7100-4fbe-437e-bc38-1533f83a50bb)

### Step 3: Configure Lambda Function



1. **Open Lambda**: Navigate to Lambda in AWS Services.
![Screenshot (664)](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/c90b1ded-9cb8-4bd3-bc98-fb8063ae3871)

2. **New Function**: Click on **Create function**.
3. **Function Basics**: Set the name and choose Python as the runtime.

![Screenshot (665)](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/6bbad9c2-a8c4-4521-8409-829b8fca3eec)

![Screenshot (666)](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/ed8d31da-d2d5-43d3-964b-04b3d9c83307)

4.  Paste the provided Lambda code.
5.  Carefully replace bucket name with the actual name of your bucket and the region that you have selected.
6. **Lambda Code**:

   Below is a breakdown of the Lambda code:

   ```python
   # Importing necessary libraries
   import boto3
   import botocore.config
   import json
   from datetime import datetime


These imports fetch essential libraries required for the code's operation:

- `boto3`: AWS SDK for Python, which allows Python scripts to interact with AWS services like Amazon S3 and AWS Bedrock.
- `botocore.config`: Part of the Boto3 library, used to configure specific options like timeout settings and retry logic for AWS service actions.
- `json`: Standard Python library used to parse JSON data, which is the format of the event data that Lambda functions receive and the format used to send responses.
- `datetime`: Standard Python library used to work with dates and times. It's particularly useful here for timestamping generated code files before saving to S3.

  ```python
  # Function to generate code using the AWS Bedrock service
  def generate_code_using_bedrock(message:str,language:str) ->str:
    ...

This function interacts with AWS Bedrock to generate code. It prepares the prompt for Bedrock, sets up a request body, invokes the Bedrock model, and processes the response to return the generated code.

  ```python
    # Function to save the generated code to an S3 bucket
    def save_code_to_s3_bucket(code, s3_bucket, s3_key):
     ...
  ```

This function saves the generated code to a specified S3 bucket. It creates an S3 client using boto3, and puts the generated code in the specified bucket and key.

   ```python
    # Main Lambda handler function
    def lambda_handler(event, context):
      ...
```
This is the primary function triggered by AWS Lambda. It processes the event to extract necessary details, calls the generate_code_using_bedrock function to generate the code, checks if code was successfully generated, and if so, saves it to an S3 bucket. Finally, it returns a response.


### Step 4: Create a boto3 Lambda Layer for Bedrock Support

As AWS Bedrock is a newer service, it requires the latest version of `boto3` which may not be available in the standard AWS Lambda environment. Therefore, we need to create a custom Lambda layer with the latest `boto3`.

### Boto3 Lambda Layer Creation



To ensure our Lambda function has the latest `boto3` library, follow these steps:

1. I referred to this AWS documentation to manually create a Lambda layer. Here's the link for your reference: [How do I resolve "unknown service", "parameter validation failed", and "object has no attribute" errors from a Python (Boto3) Lambda function?](https://repost.aws/knowledge-center/lambda-python-runtime-errors).
2. Using AWS CloudShell, execute the necessary commands to create a new Lambda layer with the latest version of `boto3`. The list of commands and a step-by-step walkthrough can be found in the `boto3-layer.txt` file within this project repository.

![Screenshot (667)](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/421a3c38-71bc-4b74-877f-225a844cac81)

3. Make sure to copy the `LayerVersionArn`.We will be using it later.


4. Finally, attach this newly created Lambda layer to your Lambda function. Go to your Lambda function's settings, click on **Layers**, and then **Add a layer**. Choose `Specify an ARN` and paste the `LayerVersionArn` that you had copied earlier.Click on `verify` and then add it.


![Screenshot (670)](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/0cdadb20-e284-4f50-aa37-113f5e3a617b)

With this custom Lambda layer in place, your function will have access to the latest `boto3` features required to interact with AWS Bedrock.

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/efb192bf-590c-4a38-b334-ad74f4436564)


### Step 5: Integrate with API Gateway

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/68abefc9-57ae-48b5-b090-01c675220ee0)


1. **Open API Gateway**: Navigate to API Gateway.
2. **Create New API**: Initiate a new HTTP POST API.

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/820e9148-b2b0-419a-bda2-cbfa46c2c7d6)

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/b00eebd6-18b7-486b-8904-9d5f08884ee0)


3. **Define a Route**: Set a route like `/code-gen`.

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/27f982c3-041d-4ca8-8311-3ebde0e3b9df)

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/5aa9e3b1-245b-4bf3-8fdd-0eb406a9251a)


4. **Link Lambda**: Link the API to your Lambda.

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/bdbf74b6-f968-4515-9fcd-74cc7456e239)
![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/98d4ced3-62d5-40fd-a6a9-002ee6fff04a)
![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/41046f4d-08cd-47ff-9069-c1719b5061b1)



5. **Deploy**: Create a `dev` stage and deploy.

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/a6709c8a-721c-450d-bd30-5e890ed70be9)
![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/6e824a4d-4550-46ec-8591-a95cace4e7fc)

## API Deployment Best Practices

It's highly recommended to create a development stage, often named `dev`, for your API. This allows you to test changes in an isolated environment that mimics production settings but does not affect end-users. Here's how to set it up:

1. In the API Gateway console, create a new stage named `dev`.
2. Deploy your API to this stage whenever you want to test new changes.

### Disable Automatic Deployments

By default, changes to your API configuration might trigger automatic deployments. However, for better control over when and what gets deployed, you should disable automatic deployments:

1. Navigate to the `Stages` section of your API Gateway.
2. Select the stage you want to manage.
3. Find the `Automatic deployments` setting and disable it.

By disabling automatic deployments, you can manually deploy your API when you're confident the changes are ready, after thorough testing. This practice helps prevent unintended effects from immediate deployments and is particularly important in production environments.

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/3f6b40e5-8b3e-490c-8414-4a6da5565daa)

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/8cb42d7b-4bd8-455d-b75d-ac0394bd63ae)

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/5719ea8b-1f22-4116-8a9e-a68eb952f38b)

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/89fd49d5-61b4-447e-9d99-059a04fa915f)

The api has been successfully deployed.

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/daf573b3-25ff-4d8c-82d1-4bf230118aae)

Make sure to copy the Invoke URL of dev.We will be using this to call our API in later step.

![Screenshot (692)](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/a680baa6-c3d6-4143-9023-890fd35f4b46)

### Step 6: Verify Integrations with Lambda Function

After setting up the boto3 Lambda layer and the HTTP API, it is crucial to confirm that they are correctly integrated with your Lambda function. This step ensures that your Lambda function can utilize the latest boto3 features and interact with the HTTP API as expected.


![Screenshot (691)](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/986ca744-9135-4825-a95e-128c0831dbde)


### Step 7: Test Using Postman

1. **Open Postman**: Launch Postman.
2. **New Request**: Start a POST request.
3. **Input Endpoint**: Use the provided endpoint.Don't forget to enter the route specified in the api at the end.Mine is `/code-gen`
4. **Payload Configuration**: Input the JSON payload.
5. **Send Request**: Click **Send**.
![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/d234a2c7-6b99-4048-89d7-d6872ae1ca09)



### Step 8: Review in S3

1. **Open S3**: Go back to S3.
2. **Access Bucket**: Open `code-gen-bucket`.
3. **Locate Code**: Find the generated code file.

![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/d5e2ea4a-f1b0-4124-b0b0-e60622c08d8d)


4.Download the python file and open it in any editor of your choice.
![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/488a824f-8a83-4ab7-b3cd-a32b6143f509)


![image](https://github.com/Somya4746/Serverless-Code-Vault/assets/141270415/daf6aaca-c935-4bbf-b87f-548184a13ea7)

Voilà! The code has been generated.

---

## Conclusion

Serverless-Code-Vault is an efficient solution for code generation and storage. This guide assists users in setting up and leveraging this system effectively.




















