# Week 4 - Azure Cloud Fundamentals and Data Pipeline Implementation using Azure Data Factory

## Celebal Technologies Internship

### Objective

The objective of this assignment was to understand the fundamentals of Microsoft Azure Cloud and implement a complete data pipeline using Azure Storage Account and Azure Data Factory (ADF). The pipeline reads a CSV file from Azure Blob Storage, validates its metadata, and copies it to another location within Blob Storage.

---

## Azure Services Used

- Microsoft Azure Portal
- Azure Resource Group
- Azure Storage Account
- Azure Blob Storage
- Azure Data Factory (ADF)
- Azure IAM (Identity and Access Management)

---

## Dataset

**Dataset Used:** Sample Superstore Dataset

**Format:** CSV

The dataset was uploaded to Azure Blob Storage and used as the source for the Azure Data Factory pipeline.

---

## Tasks Completed

### Task 1 - Resource Group

- Created a Resource Group
- Configured the deployment region

---

### Task 2 - Azure Storage

- Created an Azure Storage Account
- Created Blob Containers
  - input
  - output
- Uploaded the Sample Superstore CSV file

---

### Task 3 - Azure Data Factory

- Created Azure Data Factory
- Configured Linked Service
- Created Source Dataset
- Created Destination Dataset
- Implemented Get Metadata activity

---

### Task 4 - Pipeline Development

Developed an Azure Data Factory pipeline consisting of:

- Get Metadata Activity
- Copy Data Activity

The pipeline copies the source CSV file from the **input** container to the **output** container.

---

### Task 5 - Pipeline Execution

- Validated the pipeline
- Executed the pipeline using Debug
- Pipeline completed successfully
- Output file generated successfully

---

### Task 6 - IAM Configuration

Assigned the following roles to Azure Data Factory Managed Identity:

- Reader
- Contributor

This allows Azure Data Factory to securely access Azure Storage resources.

---

# Mini Project

## Problem Statement

Build a complete Azure Data Factory pipeline that reads a CSV file from Azure Blob Storage and copies it to another Blob Storage location after validating metadata.

### Source

Azure Blob Storage

```
input/
└── Sample-Superstore.csv
```

### Destination

Azure Blob Storage

```
output/
└── Superstore_Copy.csv
```

---

## Pipeline Workflow

```
Sample-Superstore.csv
        │
        ▼
Azure Blob Storage (Input)
        │
        ▼
Linked Service
        │
        ▼
Source Dataset
        │
        ▼
Get Metadata
        │
        ▼
Copy Data Activity
        │
        ▼
Destination Dataset
        │
        ▼
Azure Blob Storage (Output)
```

---

## Project Outcome

- Successfully connected Azure Data Factory with Azure Blob Storage.
- Retrieved metadata from the source CSV file.
- Copied the CSV file to the destination container.
- Verified successful pipeline execution.
- Configured IAM roles for secure resource access.

---

## Technologies Used

- Microsoft Azure
- Azure Resource Group
- Azure Storage Account
- Azure Blob Storage
- Azure Data Factory
- Azure IAM

---

## Learning Outcomes

During this assignment, I learned:

- Azure Cloud fundamentals
- Azure Resource Management
- Blob Storage configuration
- Azure Data Factory architecture
- Linked Services
- Datasets
- Get Metadata activity
- Copy Data activity
- Pipeline execution and monitoring
- Azure IAM role assignment

---

## Repository Structure

```
Week-4/
│
├── Screenshots/
├── Sample-Superstore.csv
├── README.md
└── Week4_Report.pdf
```

---

## Conclusion

This assignment provided practical experience in building an end-to-end data pipeline using Microsoft Azure. By integrating Azure Blob Storage with Azure Data Factory, I gained hands-on knowledge of cloud-based ETL processes, resource management, data movement, and access control using Azure IAM.