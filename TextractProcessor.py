import json
import time
import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    textract = boto3.client('textract')

    bucket = "doc-summary-inputs-project"
    key = event['s3_key']

    try:
        print("Received event:", event)

        # Handle PDF separately
        if key.lower().endswith(".pdf"):
            print("Processing as PDF...")

            # Start Textract async job
            start_response = textract.start_document_text_detection(
                DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': key}}
            )
            job_id = start_response['JobId']
            print(f"Started job with ID: {job_id}")

            # Wait for job to finish (basic polling loop)
            while True:
                result = textract.get_document_text_detection(JobId=job_id)
                status = result['JobStatus']
                print("Job status:", status)
                if status in ['SUCCEEDED', 'FAILED']:
                    break
                time.sleep(2)

            if status == 'FAILED':
                raise Exception("Textract job failed.")

            # Extract text from all pages
            pages = []
            next_token = None
            while True:
                response = textract.get_document_text_detection(
                    JobId=job_id,
                    NextToken=next_token
                ) if next_token else result

                pages.extend([
                    b['Text'] for b in response['Blocks']
                    if b['BlockType'] == 'LINE'
                ])

                next_token = response.get('NextToken')
                if not next_token:
                    break

            text = ' '.join(pages)

        else:
            print("Processing as image...")

            # For single-page images
            response = textract.detect_document_text(
                Document={'S3Object': {'Bucket': bucket, 'Name': key}}
            )

            lines = [b['Text'] for b in response['Blocks'] if b['BlockType'] == 'LINE']
            text = ' '.join(lines)

        # Return extracted text along with input
        return {
            "statusCode": 200,
            "body": json.dumps({
                "text": text,
                **event
            })
        }

    except Exception as e:
        print("Error occurred:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e),
                "event": event
            })
        }
