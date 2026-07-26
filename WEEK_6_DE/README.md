# Week 6 – Apache Spark Assignment

## Celebal Technologies Internship – Week 6

This repository contains the solutions for the Week 6 internship assignment on **Apache Spark**. The notebook demonstrates Spark fundamentals, DataFrame operations, CSV and Parquet file handling, transformations, actions, filtering, schema management, and Spark architecture concepts.

---

## Assignment Objectives

- Understand Apache Spark Architecture
- Learn the roles of Driver, Cluster Manager, and Executors
- Explore Spark's Lazy Evaluation mechanism
- Perform DataFrame operations using PySpark
- Read and write CSV and Parquet files
- Apply filtering, selection, renaming, and type casting
- Understand Transformations and Actions
- Learn about DAG (Lineage Graph) and Fault Tolerance
- Explore Predicate Pushdown in Parquet
- Compare Client Mode and Cluster Mode

---

## Topics Covered

### Spark Architecture
- Driver Program
- Cluster Manager
- Executors
- Client Mode
- Cluster Mode
- DAG (Directed Acyclic Graph)
- Fault Tolerance

### Data Processing
- Reading CSV Files
- Reading Parquet Files
- Writing CSV Files
- Writing Parquet Files
- Schema Inference
- Column Selection
- Data Filtering
- Column Renaming
- Data Type Casting
- Creating New Columns

### Performance Concepts
- Lazy Evaluation
- Predicate Pushdown
- Transformations vs Actions
- show() vs collect()

---

## Assignment Questions Covered

- ✔ Q1 – Driver, Cluster Manager and Executor
- ✔ Q2 – Lazy Evaluation
- ✔ Q3 – Read CSV with Header and Infer Schema
- ✔ Q4 – CSV vs Parquet
- ✔ Q5 – Select Required Columns
- ✔ Q6 – Rename Column and Cast Data Type
- ✔ Q7 – DAG and Fault Tolerance
- ✔ Q8 – Filter using AND Condition
- ✔ Q9 – Predicate Pushdown
- ✔ Q10 – Add Calculated Column
- ✔ Q11 – Transformations vs Actions
- ✔ Q12 – Read Parquet → Filter → Save CSV
- ✔ Q13 – Client Mode vs Cluster Mode
- ✔ Q14 – Filter using OR Condition
- ✔ Q15 – show() vs collect()

---

## Technologies Used

- Python 3.x
- Apache Spark (PySpark)
- Jupyter Notebook
- Pandas (where required)

---

## Repository Structure

```
Week6-Spark-Assignment/
│
├── week_6_cei.ipynb
├── Employee.csv
├── Processed_Employee_CSV/
├── Processed_Employee_Parquet/
├── README.md
└── screenshots/
```

---

## How to Run

### Install PySpark

```bash
pip install pyspark
```

### Start Jupyter Notebook

```bash
jupyter notebook
```

### Open

```
week_6_cei.ipynb
```

Execute all cells sequentially.

---

## Key Learnings

- Understanding Spark Architecture
- Working with DataFrames
- Reading and Writing CSV/Parquet Files
- Applying Transformations and Actions
- Filtering and Selecting Data
- Column Manipulation
- Spark Performance Optimization
- Fault Tolerance using DAG
- Efficient Data Storage using Parquet

---

## Output

The notebook demonstrates:

- Reading structured datasets
- Displaying DataFrames
- Applying filters
- Renaming columns
- Casting data types
- Creating derived columns
- Saving processed datasets in CSV and Parquet formats
- Exploring Spark execution concepts

---

## Conclusion

This assignment provides hands-on experience with Apache Spark and PySpark by implementing common data engineering operations while understanding Spark's execution model, optimization techniques, and distributed processing architecture.

---

## Author

**Pranav Balasaheb Deokar**

B.Tech Computer Science Engineering (AI & ML Honours)

Celebal Technologies Internship – Week 6