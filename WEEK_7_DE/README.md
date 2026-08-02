# Delta Lake MERGE Implementation

## Overview

This project demonstrates incremental data processing using **Delta Lake MERGE** with **Apache Spark (PySpark)**. The implementation performs basic data cleaning, creates a Delta table, simulates incremental data, and uses the MERGE operation to update existing records while inserting new records.

---

## Objective

The objective of this assignment is to understand how Delta Lake handles incremental data processing using the MERGE command.

The project includes:
- Loading data into a Delta table
- Basic data cleaning
- Creating an incremental dataset
- Performing MERGE (Update + Insert)
- Validating the final output

---

## Technologies Used

- Python
- Apache Spark (PySpark)
- Delta Lake
- Jupyter Notebook

---

## Project Structure

```
delta-lake-assignment/
│
├── data/
│   ├── customer_master.csv
│   └── customer_incremental.csv
│
├── notebooks/
│   └── delta_merge_assignment.ipynb
│
├── screenshots/
│   ├── data_loading/
│   ├── data_cleaning/
│   ├── merge_operation/
│   ├── validation/
│   └── final_output/
│
└── README.md
```

---

## Workflow

### 1. Load Dataset
- Read the customer master dataset using Spark.
- Display the dataset for verification.

### 2. Data Cleaning
- Remove duplicate records.
- Handle missing values.
- Prepare clean data for Delta Lake.

### 3. Create Delta Table
- Store the cleaned dataset as a Delta table.

### 4. Load Incremental Dataset
- Read the incremental customer dataset.
- This dataset contains:
  - Existing records to update
  - New records to insert

### 5. Perform MERGE Operation

The Delta MERGE command performs:

- **UPDATE**
  - Updates existing records based on matching Row ID.

- **INSERT**
  - Inserts records that do not already exist.

### 6. Validation

After the MERGE operation:
- Verify total row count.
- Check for duplicate Row IDs.
- Display the final merged dataset.

---

## Expected Output

- Clean Delta Table
- Existing records updated
- New records inserted
- No duplicate Row IDs
- Final merged dataset displayed successfully

---

## How to Run

1. Open the Jupyter Notebook.
2. Install the required packages:
   ```
   pip install pyspark delta-spark
   ```
3. Run all notebook cells sequentially.
4. Verify the output after the MERGE operation.
5. Capture screenshots for submission.

---

## Screenshots Included

- Data Loading
- Data Cleaning
- Incremental Dataset
- MERGE Execution
- Validation
- Final Output

---

## Learning Outcomes

After completing this assignment, you will understand:

- Delta Lake fundamentals
- Creating Delta tables
- Incremental data processing
- MERGE (UPSERT) operations
- Basic data validation using Spark

---

## Author

**Pranav Deokar**