import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # Use 'parsed' block
    parsed = event["parsed"]

    user_id = parsed["user_id"]
    summary_id = parsed["summary_id"]
    summary_text = parsed["summary"]
    file_type = parsed["file_type"]

    # Save summary to S3
    s3 = boto3.client('s3')
    summary_key = f"{user_id}/{summary_id}-summary.txt"
    s3.put_object(Bucket="doc-summary-outputs-nivas", Key=summary_key, Body=summary_text)

    # Save summary metadata to DynamoDB
    ddb = boto3.client('dynamodb')
    ddb.put_item(
        TableName="DocumentSummaries",
        Item={
            "UserId": {"S": user_id},
            "timestamp": {"S": datetime.utcnow().isoformat()},
            "SummaryId": {"S": summary_id},
            "SummaryTextS3Key": {"S": summary_key},
            "InputType": {"S": file_type},
            "SummarySnippet": {"S": summary_text[:100]}
        }
    )

    return {
        "status": "stored",
        "summary_key": summary_key
    }
