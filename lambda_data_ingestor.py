import json
import boto3
import urllib3
from datetime import datetime

# Replace with your actual Kinesis Firehose delivery stream name
FIREHOSE_NAME = 'PUT-S3-uBfM9'

def lambda_handler(event, context):
    # Initialize the HTTP client to make API requests
    http = urllib3.PoolManager()

    # Initialize the Firehose client for AWS Kinesis Firehose operations
    fh = boto3.client('firehose')

    # List of company tickers to fetch data for
    companies_list = ['AMZN', 'TSLA', 'NVDA', 'GS-PI', 'IBM']

    results = []
    # Get the current date
    current_date = datetime.now()
    # Format the date
    formatted_date = current_date.strftime("%B %d %Y")
    old_date="June 01 2020"
    # Loop through each company and fetch data from the API
    for company in companies_list:
        # Construct the API URL to fetch company data
        api_url = f"https://stock-market-data-manage.onrender.com/getSingleStockDetailsInDepth?symbol={company}&start_date={old_date}&end_date={formatted_date}"
        

        # Execute the HTTP GET request to the API
        response = http.request("GET", api_url)
        
        # Check if the API request was successful
        if response.status == 200:
            # Convert the API response from JSON format to a Python dictionary
            data_dict = json.loads(response.data.decode('utf-8'))
            
            # Add a current timestamp and the company ticker to the data dictionary
            data_dict['row_ts'] = datetime.now().isoformat()
            data_dict['company'] = company

            # Serialize the data dictionary back to a JSON string and encode to bytes
            msg = json.dumps(data_dict) + '\n'
            encoded_msg = msg.encode('utf-8')
            
            # Send the processed data to the specified Firehose delivery stream
            put_response = fh.put_record(
                DeliveryStreamName=FIREHOSE_NAME,
                Record={'Data': encoded_msg}
            )

            # Check if put_record was successful
            if put_response['ResponseMetadata']['HTTPStatusCode'] == 200:
                results.append(f"Success: Data for {company} sent to Firehose.")
                
            else:
                results.append(f"Error: Failed to send data for {company} to Firehose.")

    # Return the results of put_record operations
    return {
        "status": "Completed",
        "results": results
    }