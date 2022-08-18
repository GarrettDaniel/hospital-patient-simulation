# hospital-patient-simulation
This repo shows a proof-of-concept architecture for simulating hospital ER patient data ETL and visualization at scale in near-real-time using AWS services and custom code.

The AWS architecture is as follows: (add architecture)

The code in this repo represent a Python app for custom data simulation, and a Lambda function for data enrichment (i.e. determining if patient metrics are in healthy ranges or not, and updating the dataset).  

Other aspects of the architecture were created manually in the AWS Management Console for demo/experimentation purposes, and are not included in this repo.
- EC2 Instance for running the data generation app
- S3 buckets for storing raw and enriched patient data
- SQS queue for managing data enrichment jobs
- Glue Crawler to infer data schema in S3
- Athena for querying data directly in S3
- QuickSight for data visualization and dashboard creation

For future improvements: 
- The full architecture could be packaged together using infrastructure-as-code with Terraform or AWS CloudFormation
- The Python app could be containerized with Docker, and run using ECS with Fargate instead of running on an EC2 instance
- The data generation app could be improved with more sophisticated and comprehensive patient metrics, with more realistic distributions/variation
- Data visualizations could be more sophisticated and detailed
