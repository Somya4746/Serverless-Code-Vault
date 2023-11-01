# Importing necessary libraries
import boto3
import botocore.config
import json
from datetime import datetime

# Function to generate code using the AWS Bedrock service
def generate_code_using_bedrock(message:str,language:str) ->str:
    
    # Preparing the prompt text for Bedrock
    prompt_text = f"""Human: Write {language} code for the following instructions: {message}.
    Assistant:
    """
    
    # Setting up the request body for Bedrock
    body = {
        "prompt": prompt_text,
        "max_tokens_to_sample": 2048,
        "temperature": 0.1,
        "top_k":250,
        "top_p": 0.2,
        "stop_sequences":["\n\nHuman:"]
    }

    try:
        # Creating a Bedrock client
        bedrock = boto3.client("bedrock-runtime",
        region_name="us-east-1",
        config = botocore.config.Config(read_timeout=300, retries = {'max_attempts':3})
        )
        
        # Invoking the Bedrock model
        response = bedrock.invoke_model(body=json.dumps(body),modelId="anthropic.claude-v2")
        
        # Parsing the response
        response_content = response.get('body').read().decode('utf-8')
        response_data = json.loads(response_content)
        code = response_data["completion"].strip()
        return code   # Returning the generated code

    except Exception as e:
        print(f"Error generating the code: {e}")
        return ""
        
        
# Function to save the generated code to an S3 bucket
def save_code_to_s3_bucket(code, s3_bucket, s3_key):

    s3 = boto3.client('s3')     # Creating an S3 client

    try:
        # Saving the code to the specified S3 bucket and key
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body = code)
        print("The code has been saved to s3")

    except Exception as e:
        print("Error while saving the code to s3")


# Main Lambda handler function
def lambda_handler(event, context):
    event = json.loads(event['body'])   # Parsing the event body
    message = event['message']  # Extracting the message
    language = event['key']  # Extracting the language
    print(message, language)

    generated_code = generate_code_using_bedrock(message, language)     # Generating code

    if generated_code:
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f'code-output/{current_time}.py'       # Preparing the S3 key
        s3_bucket = 'code-gen-bucket'       # Specifying the S3 bucket   

        save_code_to_s3_bucket(generated_code,s3_bucket,s3_key)

    else:
        print("No code was generated")
        
        
    # Returning a success response
    return {
        'statusCode':200,
        'body':json.dumps('Code generation')

    }
