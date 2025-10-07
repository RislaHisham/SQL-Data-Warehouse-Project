# Sales Data Warehouse Project
Project Overview

This project demonstrates the design and implementation of a Data Warehouse solution for a fictional organization’s sales data. The raw sales data is extracted from source systems and transformed into structured tables to enable efficient analysis and reporting. The solution integrates data processing, storage, and visualization to generate actionable insights for business decisions.

Key Objectives:

Design a scalable and organized data warehouse for sales data.

Transform raw data into clean, structured tables ready for analytics.

Create meaningful reports and visualizations using Power BI.

# 1. Architecture Layers

Data Source Layer

Raw sales data provided in CSV/Excel format.

Could represent transactional systems like ERP, CRM, or POS systems.

Staging Layer

Temporary storage of raw data.

Data is cleaned, validated, and pre-processed for transformation.

Data Warehouse Layer

Fact Table: FactSales

Contains transactional sales data: SalesID, DateID, ProductID, CustomerID, Quantity, Revenue, Discount, etc.

Dimension Tables:

DimDate – Stores date details (Year, Month, Quarter, Day).

DimCustomer – Stores customer information (Name, Location, Segment).

DimProduct – Stores product information (Category, Subcategory, Brand).

DimSalesperson – Stores sales representative details (Name, Region, Team).

Presentation / Reporting Layer

Power BI dashboards visualize sales trends, top products, revenue by region, and KPIs.

Users can filter, drill down, and analyze data for strategic insights.
