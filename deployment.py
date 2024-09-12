import boto3

cfn = boto3.client('cloudformation')

GlobalTableName = 'ka-me-ha-me-ha-archives'
Region1 = 'us-west-2'
Region2 = 'ap-south-1'
BucketName = 'ka-me-ha-me-ha-bucket'
LambdaFunctionName = 'ka-me-ha-me-ha-enabler'

# Bucket Stack
print('Creating S3 bucket Cloudformation Stack.......')
bucket_stack = cfn.create_stack(
    StackName='S3-Bucket-Stack',
    TemplateURL='https://my-code-for-task.s3.ap-south-1.amazonaws.com/ka-me-ha-me-ha-bucket.yaml',
    Parameters=[{
        'ParameterKey': 'BucketName',
        'ParameterValue': BucketName
    }]
)

waiter = cfn.get_waiter('stack_create_complete')
waiter.wait(StackName=bucket_stack['StackId'])

print('Bucket stack created successfully')
print(f"Bucket-ID : {bucket_stack['StackId']}")
print()

# Dynamodb Stack
print("Creating Dynamodb Cloudformation Stack.......")
dynamodb_stack = cfn.create_stack(
    StackName='DynamoDb-Stackk',
    TemplateURL='https://my-code-for-task.s3.ap-south-1.amazonaws.com/ka-me-ha-me-ha-archives.yaml',
    Parameters=[{
        'ParameterKey': 'GlobalTableName',
        'ParameterValue': GlobalTableName
    },{
        'ParameterKey': 'Region1',
        'ParameterValue': Region1
    },{
        'ParameterKey': 'Region2',
        'ParameterValue': Region2
    }
    ]
)

waiter.wait(StackName=dynamodb_stack['StackId'])

print('Dynamodb stack created successfully')
print(f"Dynamodb-Stack-ID : {dynamodb_stack['StackId']}")
print()


# Lambda Role Stack
print('Creating Lambda Role Cloudformation Stack.......')
lambda_role_stack = cfn.create_stack(
        StackName='Lambda-Role-Stack',
        TemplateURL='https://my-code-for-task.s3.ap-south-1.amazonaws.com/lambda-role.yaml',
        Parameters=[{
            'ParameterKey': 'GlobalTableName',
            'ParameterValue': GlobalTableName
        },{
            'ParameterKey': 'Region1',
            'ParameterValue': Region1
        },{
            'ParameterKey': 'Region2',
            'ParameterValue': Region2
        },{
            'ParameterKey': 'S3BucketName',
            'ParameterValue': BucketName
        }],
        Capabilities=['CAPABILITY_NAMED_IAM']
)

waiter.wait(StackName=lambda_role_stack['StackId'])

print('Lambda Role created successfully')
print(f"Lambda-Role-Stack-ID : {lambda_role_stack['StackId']}")
print()

#  LambdaStack
print('Creating Lambda functions Cloudformation Stack.......')
lambda_function_stack = cfn.create_stack(
        StackName='Lambda-Stack',
        TemplateURL='https://my-code-for-task.s3.ap-south-1.amazonaws.com/ka-me-ha-me-ha-enabler.yaml',
        Parameters=[{
            'ParameterKey': 'LambdaFunctionName',
            'ParameterValue': 'ka-me-ha-me-ha-enabler'
        }]
)

waiter.wait(StackName=lambda_function_stack['StackId'])

print('Lambda created successfully')
print(f"Lambda-Function-Stack-ID : {lambda_function_stack['StackId']}")
print()
print('Deployment completed successfully')