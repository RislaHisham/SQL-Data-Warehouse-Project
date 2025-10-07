# Sales Data Warehouse Project
Project Overview

This project demonstrates the design and implementation of a Data Warehouse solution for a fictional organization’s sales data. The raw sales data is extracted from source systems and transformed into structured tables to enable efficient analysis and reporting. The solution integrates data processing, storage, and visualization to generate actionable insights for business decisions.

Key Objectives:

Design a scalable and organized data warehouse for sales data.

Transform raw data into clean, structured tables ready for analytics.

Create meaningful reports and visualizations using Power BI.

# 1. Architecture Layers

* Data Source Layer

Raw sales data provided in CSV/Excel format.

Could represent transactional systems like ERP, CRM, or POS systems.

* Staging Layer

Temporary storage of raw data.

Data is cleaned, validated, and pre-processed for transformation.

* Data Warehouse Layer

** Fact Table: FactSales

   // Contains transactional sales data: SalesID, DateID, ProductID, CustomerID, Quantity, Revenue, Discount, etc.

** Dimension Tables:

   // DimDate – Stores date details (Year, Month, Quarter, Day).

   // DimCustomer – Stores customer information (Name, Location, Segment).

   // DimProduct – Stores product information (Category, Subcategory, Brand).


* Presentation / Reporting Layer

Power BI dashboards visualize sales trends, top products, revenue by region, and KPIs.

Users can filter, drill down, and analyze data for strategic insights.

# 2. Project Steps
Step 1: Data Understanding & Profiling

* Examine raw sales data for structure, missing values, duplicates, and inconsistencies.

* Identify key columns needed for analysis (e.g., OrderID, Date, Product, Customer, Revenue).

Step 2: Data Warehouse Design

* Design star schema for fact and dimension tables.

* Define primary keys and foreign keys for efficient joins.

* Ensure scalability for additional data sources in the future.

Step 3: Data Transformation

* Use Python and SQL scripts to:

* Clean data (remove duplicates, handle nulls).

* Derive necessary columns (e.g., Year, Month, Quarter).

* Populate dimension tables.

* Aggregate and insert data into the fact table.

Step 4: Power BI Dashboard

* Connect Power BI to the Data Warehouse.

* Build visuals to display:

    // Total Revenue, Total Orders

    // Sales by Product, Region, and Customer Segment

    // Trend analysis over months/years

* Implement slicers and filters for interactive reporting.


# 3. Technologies Used

* Database / Storage: PostgreSQL, SQL Server, or CSV files for demonstration

* Data Transformation: Python (pandas), SQL

* Visualization: Power BI

* Version Control:  GitHub

# 4. Deliverables

* Data Warehouse Design: ER diagram and table structures.

* Scripts: Python/SQL scripts to transform raw data into fact & dimension tables.

* Power BI Dashboard: Interactive dashboard with insightful sales analytics.

* Data Dictionary: Excel file describing table structures, columns, and data types.
