# Data-Monitoring-with-AWS
Serverless GitHub Watchtower project that monitors the health and availability of live GitHub public activity data.
## Project Overview
The project focuses on monitoring and alerting based on activity volume.
- Periodically ingests data from the GitHub Public Events API
- Stores raw responses in Amazon S3
- Sends automated email alerts via Amazon SNS when data quality issues are detected.
## Architecture
    EventBridge Scheduler (12-hour schedule)
            ↓
    AWS Lambda (ingestion + validation)
            ↓
    Amazon S3 (raw data storage)
            ↓
    Amazon SNS (email alerts)

## Requirements
- Languages: Python 3.12+
- Libraries: boto3, json, orllib.request
- Cloud Platform: AWS
  - S3 for raw JSON storage
  - AWS EventBridge for scheduled requests
  - AWS Lambda for API requests, raw JSON ingestion, and conditional alert
  - AWS SNS
## Note

