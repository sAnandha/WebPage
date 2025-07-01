import json
import boto3

def lambda_handler(event, context):
    # Support both direct and wrapped inputs
    if 'body' in event:
        try:
            body = json.loads(event['body'])
        except:
            body = event['body']
    else:
        body = event

    if 'text' not in body:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing "text" field in input.'})
        }

    user_input = body['text']

    bedrock = boto3.client('bedrock-runtime')

    prompt_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {
                "role": "user",
                "content": f"Please summarize the following:\n{user_input}"
            }
        ],
        "max_tokens": 200,
        "temperature": 0.3
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(prompt_body)
    )

    result = json.loads(response['body'].read())

    return {
        'statusCode': 200,
        'body': json.dumps({
            'summary': result['content'][0]['text'],
            'user_id': body['user_id'],
            'summary_id': body['summary_id'],
            'file_type': body['file_type']
        })
    }
