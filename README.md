# Import CSV files in S3 to DynamoDB table by AWS Glue

Inspired by https://github.com/awslabs/aws-glue-blueprint-libs/tree/master/samples/s3_to_dynamodb

## How
* Create a new AWS Glue Job with `Spark script editor` and `Create a new script with boilerplate code` as option
* Copy/paste `s3_to_dynamodb.py` code
* Modify S3 path and target Dynamodb table name
* Save script and run
* The AWS Glue Job can be scheduled with cron job to run
* IAM role for the job need to have DynamoDB, S3 bucket access and `AWSGlueServiceRole` (AWS managed)

## Important Note
* AWS Glue Job with current script cannot delete old records. e.g. First imported csv has 3 records but second imported has only 2 of the previous records. Glue won't delete the one shouldn't exist. 
* DynamoDB expireAt can be implemented as a lambda invoked by S3 upload, then add expire at column and save in a new S3 path where Glue import from.
* AWS Glue Job can be triggered by CLI. e.g. `aws glue start-job-run --job-name {job name e.g. test} --region us-west-2`
* The script can use custom params. Refer to [AWS Glue Script Params](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-get-resolved-options.html)
* Terraform implementation:
  * Create a S3 bucket to host python scripts
  * Upload scripts via terraform.
  * Create IAM for AWS Glue Job to execute (DynamoDB, S3 bucket access and AWS managed role `AWSGlueServiceRole` )
  * Create [AWS Glue Job](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/glue_job) with script location in S3 bucket

## Full Automation Design
* Create DynamoDB table
* S3 upload trigger lambda to add expireAt colum for csv file, then save in a new S3 path
* AWS Glue Job scheduled to run after the estimated time when lambda can finish the work previously
