import sys
import awswrangler as wr
import boto3

# Define constants for bucket and database names, and the query output location
BUCKET_TO_DEL = 'transformed-f-data'
DATABASE_NAME = 'financial_data_db'
TABLE_NAME = '"structured_fd-transformed_f_data"'  # Using double quotes for special characters
QUERY_OUTPUT_BUCKET = 's3://query-results-location-delete-tr-data/'

# Initialize AWS clients
s3_client = boto3.client('s3')
athena_client = boto3.client('athena')

# Query to check stock price logical relations
STOCK_PRICE_RELATIONS = f"""
SELECT COUNT(*) AS result_count
FROM {TABLE_NAME}
WHERE NOT (high >= open AND high >= close AND low <= open AND low <= close)
"""

# Query to check for data range anomalies
DATA_RANGE_ANOMALIES = f"""
SELECT COUNT(*) AS anomaly_count
FROM {TABLE_NAME}
WHERE adjusted_close < 0 OR close < 0 OR high < 0 OR low < 0 OR open < 0
"""

# Function to run Athena queries and handle the results
def run_query_and_check(query, database, result_field):
    try:
        response = wr.athena.read_sql_query(sql=query, database=database)
        # Check if any anomalies were found based on the result field
        if response[result_field].iloc[0] > 0:
            sys.exit(f'Quality check failed: {response[result_field].iloc[0]} issues found.')
        else:
            print(f'Quality check passed: No {result_field.replace("_count", "")} issues found.')
    except Exception as e:
        sys.exit(f'Failed to execute query: {str(e)}')

# Run the quality checks
run_query_and_check(STOCK_PRICE_RELATIONS, DATABASE_NAME, 'result_count')
run_query_and_check(DATA_RANGE_ANOMALIES, DATABASE_NAME, 'anomaly_count')
