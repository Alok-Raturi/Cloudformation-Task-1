## Task description
A DynamoDB table ka-me-ha-me-ha-archives with:

* regional availability in us-west-2 and ap-south-1
* 4 fields that have some relevance (this schema is to be generated on your own)
* meaningful partition and sort keys
* a DynamoDB stream that captures put updates

A Lambda function ka-me-ha-me-ha-enabler that is:
* triggered by the DynamoDB stream above
* parses the newly created entry as a JSON object
* Reads the JSON file teenage-mutant-ninja-turtles.json created in the S3 bucket ka-me-ha-me-ha
* Moves the value of the current key to the previous key, and puts the DynamoDB stream JSON object as a value of the current key

an S3 bucket ka-me-ha-me-ha with
* a JSON file teenage-mutant-ninja-turtles.json with the initial entry:

## Acceptance Criteria
* The resources are deployed with the mentioned functionalities and configurations
* All of the deployments are done using AWS Cloudformation stacks
* The related code is put in a repository on GitHub