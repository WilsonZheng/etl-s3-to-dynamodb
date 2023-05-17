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

dynamicFrame_node1 = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={
        "paths": ["s3://owner-airflow-etl-data-dev/acquisitionUnits/"]
    },
    format="json",
)

# Script generated for node ApplyMapping
ApplyMapping_node2 = ApplyMapping.apply(
    frame=dynamicFrame_node1,
    mappings=[
        ("unit_id.s", "string", "unit_id", "string"),
        ("integration_date.s", "string", "integration_date", "string"),
        ("acquisition_id.s", "string", "acquisition_id", "string"),
        ("expired_at.n", "string", "expired_at", "string"),
    ],
    transformation_ctx="ApplyMapping_node2",
)

glueContext.write_dynamic_frame_from_options(
    frame=ApplyMapping_node2,
    connection_type="dynamodb",
    connection_options={
        # Replace table name with target DynamoDB table created. PK/SK(optional) should be defined.
        "dynamodb.output.tableName": "acquisition-units-v2",
        "dynamodb.throughput.write.percent": "0.5"
    }
)

job.commit()
