import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext, SparkConf
from awsglue.context import GlueContext
from awsglue.job import Job
import time

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

dynamicFrame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={
        # Replace s3 path
        "paths": ["s3://owner-airflow-etl-data-dev/warehouse/owner_experience/acquisition_units/ts=20220913T090000/"]
    },
    format="csv",
    format_options={
        "withHeader": True,
        # "optimizePerformance": True,
    },
)

glueContext.write_dynamic_frame_from_options(
    frame=dynamicFrame,
    connection_type="dynamodb",
    connection_options={
        # Replace table name with target DynamoDB table created. PK/SK(optional) should be defined.
        "dynamodb.output.tableName": "testglue",
        "dynamodb.throughput.write.percent": "1.0"
    }
)

job.commit()
