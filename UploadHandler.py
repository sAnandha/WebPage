import json
import base64
import boto3
import uuid
import hashlib

def get_user_folder(email):
    return "user-" + hashlib.md5(email.encode()).hexdigest()[:8]

def lambda_handler(event, context):
    try:
        # Parse event body
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event

        # Extract fields
        file_content = base64.b64decode(body['file'])
        file_type = body['file_type']  # "text", "image", or "pdf"
        user_email = body['user_id']

        # Generate identifiers
        user_folder = get_user_folder(user_email)
        summary_id = str(uuid.uuid4())
        extension = (
            'txt' if file_type == 'text'
            else 'jpg' if file_type == 'image'
            else 'pdf'
        )
        file_key = f"{user_folder}/{summary_id}.{extension}"

        # Upload file to S3
        s3 = boto3.client('s3')
        s3.put_object(Bucket="doc-summary-inputs-project", Key=file_key, Body=file_content)

        # Prepare Step Function input
        step_input = {
            "user_id": user_folder,
            "file_type": file_type,
            "s3_key": file_key,
            "summary_id": summary_id
        }

        # Only add text if it's a text file
        if file_type == "text":
            step_input["text"] = file_content.decode("utf-8")

        # Start Step Function execution
        sf = boto3.client('stepfunctions')
        sf.start_execution(
            stateMachineArn="arn:aws:states:us-east-1:026090554634:stateMachine:SampleWorkflow",
            input=json.dumps(step_input)
        )

        return {
            'statusCode': 202,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://doc-summary-inputs-project.s3-website-us-east-1.amazonaws.com',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'message': 'Processing started.',
                'summary_id': summary_id,
                'user_folder': user_folder
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'error': str(e),
                'received_event': event
            })
        }
