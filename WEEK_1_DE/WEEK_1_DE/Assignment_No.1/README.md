# 📘 Assignment No. 1

# 🛒 Shopping Dataset Analysis using Python

---

## 📌 Introduction

This assignment involves performing **Exploratory Data Analysis (EDA)** on a shopping dataset using Python. The primary aim is to examine the dataset, prepare it for analysis through data cleaning, explore important patterns, and extract useful insights with the help of various Python libraries.

By completing this assignment, practical knowledge is gained in several key areas, including:

* Data loading and handling
* Data preprocessing
* Exploratory analysis
* Data visualization
* Feature creation

Working with this dataset also provides valuable experience in handling real-world retail data.

---

## 🎯 Objective of the Assignment

The main objectives of this assignment are:

✔ Import and explore the shopping dataset

✔ Examine the overall structure and contents of the dataset

✔ Detect and manage missing values

✔ Transform price-related fields into appropriate numeric data types

✔ Eliminate duplicate records to improve data quality

✔ Create additional features to support deeper analysis

✔ Perform Exploratory Data Analysis (EDA)

✔ Extract meaningful observations from the dataset

✔ Present trends and patterns using different visualizations

---

## 📂 Dataset Information

### Dataset Used:

**combined_dataset.csv**

The dataset contains detailed information about various shopping products, including pricing, discounts, customer ratings, and product categories.

### Important Columns in Dataset:

| Column Name   | Description                |
| ------------- | -------------------------- |
| title         | Product name               |
| category      | Product category           |
| initial_price | Original price of product  |
| final_price   | Discounted price           |
| discount      | Discount value             |
| rating        | Product rating             |
| ratings_count | Number of customer ratings |

This dataset can be used to study:

* Product pricing behavior
* Customer feedback through ratings
* Product popularity
* Discount trends
* Performance across different product categories

---

## 🛠 Libraries Used

The following Python libraries were used in this assignment:

### 1. Pandas

Used for:

* Reading the dataset
* Cleaning data
* Manipulating and organizing data

```python
import pandas as pd
```

---

### 2. NumPy

Used for:

* Mathematical computations
* Numerical and array-based operations

```python
import numpy as np
```

---

### 3. Matplotlib

Used for:

* Creating basic charts
* Visual representation of data

```python
import matplotlib.pyplot as plt
```

---

### 4. Seaborn

Used for:

* Creating attractive statistical plots
* Improving the appearance of visualizations

```python
import seaborn as sns
```

---

# 🚀 Concepts Covered in This Assignment

This assignment covers the following concepts:

* Importing Data
* Dataset Exploration
* Data Cleaning
* Handling Missing Values
* Data Type Conversion
* Removing Duplicate Records
* Feature Engineering
* Exploratory Data Analysis (EDA)
* Univariate Analysis
* Bivariate Analysis
* Category-wise Analysis
* Data Visualization
* Insight Generation

---

# 📋 Steps Performed

---

# Step 1: Data Loading

The shopping dataset was imported into a Pandas DataFrame for further analysis.

### Tasks performed:

✔ Imported all required Python libraries

✔ Loaded the CSV dataset

✔ Checked the dimensions of the dataset

✔ Examined the available column names

Example:

```python
df = pd.read_csv("combined_dataset.csv")
```

Purpose:

To successfully import the dataset so that it can be processed and analyzed.

---

# Step 2: Initial Dataset Inspection

This stage provides an overall understanding of the dataset before performing any preprocessing.

### Operations performed:

### Viewing first 5 rows:

```python
df.head()
```

Purpose:

To preview the initial records of the dataset.

---

### Viewing last 5 rows:

```python
df.tail()
```

Purpose:

To inspect the ending records.

---

### Checking dataset information:

```python
df.info()
```

Purpose:

To understand:

* Total number of records
* Available columns
* Data types of each column

---

### Checking missing values:

```python
df.isnull().sum()
```

Purpose:

To identify missing or null entries in every column.

---

### Statistical summary:

```python
df.describe()
```

Purpose:

To obtain descriptive statistics such as:

* Mean
* Minimum
* Maximum
* Standard Deviation

---

# Step 3: Data Cleaning

Before analysis, the dataset was cleaned to improve its quality and consistency.

### Cleaning performed:

✔ Converted price columns into numeric format

✔ Removed currency symbols (₹)

✔ Eliminated commas

✔ Removed unwanted quotation marks

✔ Filled missing values where necessary

✔ Deleted duplicate records

Example:

```python
df['final_price'] = df['final_price'].str.replace('₹','')
```

Purpose:

To prepare the dataset for accurate calculations and analysis.

---

# Step 4: Feature Engineering

Additional columns were generated to enhance the analysis.

---

## 1. Price Difference

Formula:

```python
price_difference = initial_price - final_price
```

Purpose:

To calculate the actual amount saved after discount.

---

## 2. Popularity Score

Formula:

```python
popularity_score = rating * ratings_count
```

Purpose:

To estimate product popularity using ratings and customer engagement.

---

## 3. Discount Percentage

Formula:

```python
discount_percentage = (price_difference / initial_price) * 100
```

Purpose:

To determine the percentage discount available on each product.

---

# Step 5: Exploratory Data Analysis (EDA)

EDA was carried out to identify trends, patterns, and relationships within the dataset.

---

## 📊 Univariate Analysis

Univariate analysis focuses on examining one variable at a time.

### Performed:

* Distribution of Final Price
* Distribution of Ratings
* Product Count by Category

Charts used:

✔ Histogram

✔ Boxplot

✔ Violin Plot

Purpose:

To understand the distribution and characteristics of individual variables.

---

## 🔗 Bivariate Analysis

Bivariate analysis studies the relationship between two variables.

### Performed:

* Price vs Rating
* Discount vs Ratings Count
* Initial Price vs Final Price

Charts used:

✔ Scatter Plot

✔ Line Plot

Purpose:

To identify possible relationships and trends between variables.

---

## 🏷 Category-Level Analysis

Category-level analysis compares different product categories.

### Performed:

* Average Price by Category
* Average Rating by Category
* Total Customer Ratings by Category
* Discount Comparison by Category

Charts used:

✔ Bar Chart

✔ Pie Chart

Purpose:

To evaluate and compare the performance of different product categories.

---

# 📈 Data Visualizations Used

The following visualization techniques were used throughout the analysis:

* Histogram
* Bar Chart
* Boxplot
* Pie Chart
* Scatter Plot
* Line Plot
* Violin Plot

These visualizations made it easier to interpret the data and identify meaningful trends.

---

# 💡 Key Findings

The analysis revealed several important observations:

✔ Certain product categories have noticeably higher average prices.

✔ Products offering larger discounts tend to receive greater customer engagement.

✔ Products with better ratings generally show higher popularity.

✔ A few categories contribute significantly to the overall dataset.

✔ A moderate relationship exists between product price and customer ratings.

---

# 📊 Business Insights

The insights obtained from this analysis can assist businesses in:

* Optimizing pricing strategies
* Improving customer engagement
* Understanding consumer preferences
* Identifying high-performing product categories
* Planning more effective discount campaigns

---

# ✅ Conclusion

This assignment provided practical experience in:

* Working with real-world datasets
* Cleaning and preparing raw data
* Performing Exploratory Data Analysis (EDA)
* Creating informative visualizations
* Extracting valuable business insights

Overall, the assignment strengthened practical skills in **Python-based Data Analysis** and demonstrated the complete workflow of analyzing retail data.

---

# 👨‍💻 Submitted By

**PRANAV DEOKAR**
