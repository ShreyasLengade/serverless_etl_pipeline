import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Initialize contexts and job
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Load data from the catalog, make sure to adjust 'financial_data_db' and 'stock_data_fd_bucket_ssl' to your actual database and table name
datasource0 = glueContext.create_dynamic_frame.from_catalog(database="financial_data_db", table_name="stock_data_fd_bucket_ssl")

# Transform the data
# Flatten the JSON structure, extract 'data' array and other fields
datasource1 = datasource0.toDF()
flattened = datasource1.selectExpr("company", "row_ts", "explode(data) as data").select("company", "row_ts", "data.*")

# Convert back to dynamic frame
dynamic_frame_write = DynamicFrame.fromDF(flattened, glueContext, "dynamic_frame_write")

# Write the data back to S3 (in a format Athena can query)
sink = glueContext.write_dynamic_frame.from_options(
    frame = dynamic_frame_write,
    connection_type = "s3",
    connection_options = {"path": "s3://transformed-f-data/"},
    format = "parquet"
)

job.commit()
