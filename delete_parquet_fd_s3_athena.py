import time
import boto3
import sys

# Setting up the Athena client
athena_client = boto3.client('athena')
database_to_delete = 'financial_data_db'
table_to_delete = 'structured_fd-transformed_f_data'
query_output_bucket = 's3://query-results-location-delete-tr-data/'

# Drop the table
query = f"DROP TABLE IF EXISTS `{database_to_delete}`.`{table_to_delete}`;"
response = athena_client.start_query_execution(
    QueryString=query,
    QueryExecutionContext={
        'Database': database_to_delete
    },
    ResultConfiguration={
        'OutputLocation': query_output_bucket
    }
)

query_execution_id = response['QueryExecutionId']

# Wait for the query to finish with delay
while True:
    query_status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
    query_execution_status = query_status['QueryExecution']['Status']['State']
    if query_execution_status in ["SUCCEEDED", "FAILED", "CANCELLED"]:
        break
    time.sleep(5)  # sleep for 5 seconds before checking again

# Check if query failed and handle
if query_execution_status == 'FAILED':
    error_message = query_status['QueryExecution']['Status']['StateChangeReason']
    sys.exit(f"Athena query failed with error: {error_message}")
