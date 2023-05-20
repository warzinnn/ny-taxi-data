# NY Taxi Data - DE Project

Simple ELT Pipelipe which gets data from [NY Taxi Trips,](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) transform it and make the information available for futher analysis.
- Project realized for studies purposes, along the course of [DataTalksClub - Data Engineering Zoomcamp.](https://github.com/DataTalksClub/data-engineering-zoomcamp)

### Overview
In this project, the creation and management of cloud resources was done with Terraform.
The workflow orchestration was managed by Prefect, which coordenates the Python ETL and DBT (Data transformation), along the integrations with Google Cloud Plataform to communicate with cloud services (GCS, BigQuery), and also contain an integration with discord, to notify every time the deploy was runned.
The docker images created to containerize the prefect server and prefect agent was pushed to Google Artifact Registry, and then used with Google Compute Engine to setup the compute instance which runs the prefect server and prefect agent respectively.
In the end, the data is served on Looker Studio.

### Pipeline Flow
<img width="999" alt="pipeline_final" src="https://github.com/warzinnn/ny-taxi-data/assets/102708101/34c09039-e5e7-4883-8086-0b00264ac2b6">

### Tools and Technologies Used
- [**Python**](https://www.python.org)
- [**GCP - Google Cloud Platform**](https://cloud.google.com)
    - Infrastructure as Code software (IaC): [**Terraform**](https://www.terraform.io)
    - Data Lake: [**Google Cloud Storage**](https://cloud.google.com/storage)
    - Data Warehouse: [**BigQuery**](https://cloud.google.com/bigquery)
    - [**Artifact Registry**](https://cloud.google.com/artifact-registry?hl=pt-br)
    - [**Google Compute Engine**](https://cloud.google.com/compute?hl=pt-br)
- Containerization: [**Docker**](https://www.docker.com)
- Workflow Orchestration: [**Prefect**](https://www.prefect.io/)
- Data Transformation: [**dbt**](https://www.getdbt.com)
- Data Visualization - [**Looker Studio**](https://lookerstudio.google.com/)
- Notifications Webhook: [**Discord**](https://discord.com/developers/docs/resources/webhook)

### Looker Studio Report example
<img width="1020" alt="pipeline_flow3" src="https://github.com/warzinnn/ny-taxi-data/assets/102708101/371d1e3b-95a0-45b8-8811-06e2df83d987">