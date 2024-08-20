import json
import boto3
import botocore

s3 = boto3.client('s3')

bucket_name = 'ka-me-ha-me-ha'
file_name = 'teenage-mutant-ninja-turtles.json'

file_content_format = {
    'previous': {},
    'current': {}
}


def initial_file_state():
    initial_file_content = json.dumps(file_content_format)
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=initial_file_content)
    return json.loads(initial_file_content)


def swap_data(old_data, new_data):
    new_content = json.dumps({
        'previous': old_data['current'],
        'current':  new_data
    })
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=new_content)


def lambda_handler(event, context):
    if event['Records'][0]['eventName'] != 'INSERT':
        return {
            'statusCode': 500,
            'body': json.dumps('Only INSERT will trigger this function')
        }

    else:
        new_data = event['Records'][0]['dynamodb']['NewImage']
        try:
            s3.head_object(Bucket=bucket_name, Key=file_name)
            response = s3.get_object(Bucket=bucket_name, Key=file_name)
            object_content = response["Body"].read().decode("utf-8")
            file_content = json.loads(object_content)
            swap_data(file_content, new_data)

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                file_content = initial_file_state()
                swap_data(file_content, new_data)
            else:
                print(f"Error getting S3 object: {e}")
                return {
                    'statusCode': 500,
                    'body': json.dumps('Error initializing S3 object')
                }
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully written in the file')
    }
