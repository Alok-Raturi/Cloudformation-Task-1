import json
import boto3
import botocore

s3 = boto3.client('s3')

bucket_name = 'ka-me-ha-me-ha'
file_name = 'teenage-mutant-ninja-turtles.json'


def initial_file_state():
    initial_file_content = json.dumps({
        'previous': {},
        'current': {}
    })
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=initial_file_content)
    return json.loads(initial_file_content)


def swap_data(old_data, new_data):
    new_content = json.dumps({
        'previous': old_data['current'],
        'current':  new_data
    })
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=new_content)


def lambda_handler(event, context):
    """
    ------ Sample Event Argument  -------
    {
        "Records": [
            {
                "eventID": "e6f0de19a4a55f39ca38480c4f2ede99",
                "eventName": "INSERT",
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "ap-south-1",
                "dynamodb": {
                    "ApproximateCreationDateTime": 1724239032,
                    "Keys": {
                        "Game_id": {
                            "S": "game-1"
                        },
                        "User_id": {
                            "S": "alok-1"
                        }
                    },
                    "NewImage": {
                        "Game_id": {
                            "S": "game-1"
                        },
                        "User_id": {
                            "S": "alok-1"
                        }
                    },
                    "SequenceNumber": "42600004062755084192341",
                    "SizeBytes": 52,
                    "StreamViewType": "NEW_AND_OLD_IMAGES"
                },
                "eventSourceARN":"arn:aws:dynamodb:ap-south-1:891377219026:table/ka-me-ha-me-ha-archives/stream/2024-08-21T11:03:33.380"
            }
        ]
    }
    """
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
