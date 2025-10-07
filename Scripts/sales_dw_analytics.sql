--Check schemas and tables
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'analytics'
ORDER BY table_name;

--Preview Dimension Tables (cleaned data)
SELECT * 
FROM analytics.dim_customer
ORDER BY customer_key
LIMIT 10;

SELECT * 
FROM analytics.dim_product
ORDER BY product_key
LIMIT 10;


SELECT * 
FROM analytics.dim_date
ORDER BY date_key
LIMIT 10;

-- Total Sales by Country
SELECT 
    "analytics"."dim_customer"."COUNTRY",
    ROUND(SUM("analytics"."fact_sales"."TOTALSALES")::numeric, 2) AS total_sales
FROM 
    "analytics"."fact_sales"
JOIN 
    "analytics"."dim_customer" 
ON 
    "analytics"."fact_sales"."customer_key" = "analytics"."dim_customer"."customer_key"
GROUP BY 
    "analytics"."dim_customer"."COUNTRY"
ORDER BY 
    total_sales DESC
LIMIT 10;



-- Total Sales by Product Line
SELECT 
    "analytics"."dim_product"."PRODUCTLINE",
    ROUND(SUM("analytics"."fact_sales"."TOTALSALES")::numeric, 2) AS total_sales
FROM 
    "analytics"."fact_sales"
JOIN 
    "analytics"."dim_product"
ON 
    "analytics"."fact_sales"."product_key" = "analytics"."dim_product"."product_key"
GROUP BY 
    "analytics"."dim_product"."PRODUCTLINE"
ORDER BY 
    total_sales DESC;

--Row counts for all tables
SELECT 'dim_customer' AS table_name, COUNT(*) AS row_count FROM analytics.dim_customer
UNION ALL
SELECT 'dim_product', COUNT(*) FROM analytics.dim_product
UNION ALL
SELECT 'dim_date', COUNT(*) FROM analytics.dim_date
UNION ALL
SELECT 'fact_sales', COUNT(*) FROM analytics.fact_sales;

--Check for missing foreign keys
SELECT COUNT(*) AS null_customer_keys FROM analytics.fact_sales WHERE customer_key IS NULL;
SELECT COUNT(*) AS null_product_keys  FROM analytics.fact_sales WHERE product_key IS NULL;
SELECT COUNT(*) AS null_date_keys     FROM analytics.fact_sales WHERE date_key IS NULL;

--Check total sales sum
SELECT SUM("TOTALSALES") AS total_sales_sum
FROM analytics."fact_sales";





