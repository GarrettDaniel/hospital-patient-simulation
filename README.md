# hospital-patient-simulation
This repo shows a proof-of-concept architecture for simulating hospital ER patient data ETL and visualization at scale in near-real-time using AWS services and custom code.

The code in this repo represent a Python app for custom data simulation, and a Lambda function for data enrichment (i.e. determining if patient metrics are in healthy ranges or not, and updating the dataset). Here is an example of what the raw data looks like before upload and enrichment. 

![raw_data_simulation_example](https://user-images.githubusercontent.com/36463300/185521932-101da845-1c6b-41b9-9cdf-547878eed5b7.png)

The AWS architecture is as follows:
![health-data-simulator-arch](https://user-images.githubusercontent.com/36463300/185521737-8c092b97-69ec-462a-aadf-5f34687bad03.png)

Here are some example visualizations made with QuickSight:
Monitoring all patients in aggregate
![dashboard-blood-pressure-oxygen](https://user-images.githubusercontent.com/36463300/186735753-d330d7a2-2826-4892-bf65-b5329cbb70e4.png)

Monitoring individual patients over time
![individual-patient-monitoring](https://user-images.githubusercontent.com/36463300/186735767-a311becf-9c0d-4962-a88e-b5cf34cc0985.png)

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
