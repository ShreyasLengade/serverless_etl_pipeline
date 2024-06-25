# Stock Data Ingestion and Visualization Pipeline
## Project Overview
This project establishes a robust data pipeline using AWS services to ingest, transform, and visualize stock market data. By leveraging serverless and managed services, the architecture ensures scalability, maintainability, and efficiency.

### Architecture
The pipeline is designed around several core AWS services:
<ol>
<li><b>AWS Lambda</b>: Interacts with an external API to fetch real-time stock market data.</li>
<li><b>Amazon Kinesis Data Firehose</b>: Streams data efficiently into AWS S3 for durable storage.</li>
<li><b>AWS S3</b>: Acts as a central repository to store the ingested stock market data in raw format.</li>
<li><b>AWS Glue</b>: Manages data cataloging and runs ETL (Extract, Transform, Load) jobs to transform raw data into a query-optimized format.</li>
<li><b>AWS Athena</b>: Used for running SQL queries against the data stored in S3, leveraging the serverless capabilities to handle large datasets.</li>
<li><b>Grafana</b>: Visualizes the transformed data to provide insights into stock market trends, connected to AWS Athena as the data source.</li>
</ol>
<img src="https://github.com/ShreyasLengade/Github-Images/blob/2d55913c4815760992e77fcec98f6f4d2302cca6/Architecture.jpg">

#### Data Flow
<ol>
<li><b>Data Ingestion</b>: The data ingestion begins with an external API call to https://stock-market-data-manage.onrender.com/ which provides detailed stock market data. The data includes various stock attributes such as open, high, low, close, adjusted close, and volume.</li>
<li><b>Lambda Function</b>: An AWS Lambda function is triggered periodically by an EventBridge schedule to call the external API and retrieve the latest data.</li>
<li><b>Kinesis Data Firehose</b>: The Lambda function pushes the data to Amazon Kinesis Data Firehose, which then streams this data to an S3 bucket.</li>
<li><b>Data Transformation</b>: AWS Glue is employed to catalog the data and run transformation jobs converting the raw data into a more analytics-friendly format (Parquet) that is optimized for quick retrieval and analysis.</li>
<li><b>Visualization</b>: Finally, the processed data is visualized using Grafana, providing dynamic and real-time insights into market trends and performance.</li>
</ol>  

#### Project Goals
The primary goal of this project is to demonstrate the capabilities of AWS services in building an effective ETL pipeline, emphasizing the architectural choices and integrations necessary for real-time data processing and visualization in the cloud.

##### Tools and Technologies Used
AWS Lambda, AWS Kinesis, AWS S3, AWS Glue, AWS Athena, Grafana, and Python.

<h1> Getting Started with the Stock Data Ingestion and Visualization Pipeline</h1>
<h2>PART 1: Data Ingestion</h2>
<h3>Objective: Extract data from external sources and ingest it into AWS.</h3>
Steps:
<ol>
<li>AWS S3 and Athena Setup:
<ul>
<li>Amazon S3 buckets: Create S3 buckets to store raw data. This data can be accessed by various AWS services throughout the pipeline.</li>
<li>AWS Athena: Use Athena's serverless query editor to analyze data directly in S3, providing a powerful tool for exploring and querying large datasets without server management.</li></ul>
</li>
<li>Data Ingestion Using Lambda:
<ul><li>AWS Lambda: Implement Python scripts in Lambda functions to fetch data from https://stock-market-data-manage.onrender.com/. Lambda allows running code without provisioning servers, handling the scaling automatically.
<img src="https://github.com/ShreyasLengade/Github-Images/blob/d5dfcae39298a803a44ec45a1fb629770e9c06fa/Lambda.jpg">
</li>
<li>Automating Lambda Execution: EventBridge Triggers: Set up AWS EventBridge to trigger Lambda functions at specified intervals, ensuring regular data updates without manual intervention.</li>  
  <br>
<li>Data Storage: The data fetched is then pushed to the configured S3 bucket.
<img src="https://github.com/ShreyasLengade/Github-Images/blob/4c4aa25500cffb43e3adc28aad500e2c4d0ce19a/S3_fd_bucket.png">
</li></ul>
</li>  
</ol>

<h2>PART 2: Data Transformation</h2>
<h3>Objective: Organize and optimize the ingested data for analysis and visualization by transforming it into an efficient format and ensuring data integrity before visualization.</h3>
Steps:
<ol>
<li>Batching Data with AWS Firehose:
<ul><li>AWS Firehose: Set up Firehose to collect and batch incoming data, streamlining the process of loading large volumes of data into S3. Firehose is configured to automatically partition the incoming data before it is stored, making future queries more efficient.</li></ul>
</li>
<li>
  Table Creation with Glue Crawler:
  <ul><li>AWS Glue Crawler: Employ the Glue Crawler to automatically scan the batched data stored in S3 and create metadata tables in the AWS Glue Data Catalog. This step is essential for organizing data into a searchable and manageable format.</li></ul></li>
<li>Data Preparation with Glue Jobs:
<ul>
<li>Parquet Conversion: Configure Glue jobs to transform the batched data into the Parquet format. Parquet is chosen for its efficiency in storing columnar data, which significantly enhances both data compression and query performance.</li>
<li>Workflow Management:  Implement a series of Glue jobs orchestrated within a Glue workflow to systematically process the data:
<ul>
<li>Data Crawling: Crawl new data to update the Glue Data Catalog with the latest datasets.</li>
<li>Data Cleaning: Remove outdated or redundant data from S3 to maintain data hygiene.</li>
<li>Table Optimization: Create optimized data tables in Parquet format that are structured for quick access and analysis.</li>
<li>Data Quality Assurance: Perform quality checks on the transformed data to ensure accuracy and consistency before it moves to production storage.</li>
<li>Data Finalization: Store the fully processed and verified data in a designated 'prod_s3_bucket' that serves as the final repository for data ready for analysis.</li>
</ul>
</li>
</ul>
</li>
<li>
Workflow Orchestration:
<ul><li>AWS Glue Workflow: Before the data visualization stage, orchestrate a comprehensive workflow using AWS Glue. This workflow manages the sequence of tasks from data ingestion to storage, ensuring that data flows seamlessly through each phase of the ETL process. It includes triggers for each job, error handling mechanisms, and dependency resolution to ensure that data is processed efficiently and correctly, ready for the next stage.</li>
<li>Monitoring and Logs: Utilize AWS CloudWatch to monitor the execution of the workflow and log all activities. This enables troubleshooting and optimization of the ETL process, ensuring high reliability and performance.</li>
  <img src="https://github.com/ShreyasLengade/Github-Images/blob/c058fdfc70d0c01135fb17ab456e064b6ef27247/Glue.png"><br>
  <img src="https://github.com/ShreyasLengade/Github-Images/blob/98fedb8ebd45aa3659996b74ce22375744f954bc/Workfliw.png">
</ul>
</li>
<li>
Data Visualization Preparation: Integration with Grafana: Prepare the transformed and curated data for visualization by setting up integrations between the production data in 'prod_s3_bucket' and Grafana through AWS Athena. This setup allows for dynamic querying and visualization of the data, enabling users to generate real-time insights from the processed stock market data. 
<img src="https://github.com/ShreyasLengade/Github-Images/blob/4d1c93bceb32a840b9fd1913b008b16c4590a298/visaulisaiton.png"><br>
</li>
</ol>
