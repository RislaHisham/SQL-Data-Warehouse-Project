# ============================================================
#  Libraries
# ============================================================
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import date

# ============================================================
# 1️⃣ Database Connection
# ============================================================
DB_USER = "postgres"
DB_PASS = "12345678"  
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "sales_dw"

# Create SQLAlchemy connection engine
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# ============================================================
# 2️⃣ Ensure Schemas Exist
# ============================================================
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS stg;"))
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS analytics;"))
    conn.commit()
print("✅ Schemas created successfully")

# ============================================================
# 3️⃣ Load Raw CSV
# ============================================================
csv_path = r"C:\Users\DELL\Downloads\sales_data_sample.csv"  # Update path
df = pd.read_csv(csv_path, encoding="latin1")
print(f"📂 Loaded CSV with {len(df)} rows")

df.to_sql("sales_data", engine, schema="raw", if_exists="replace", index=False)
print("✅ Loaded data into raw.sales_data")

# ============================================================
# 4️⃣ Transformations — Clean + Enrich
# ============================================================

# --- Clean column names ---
df.columns = [c.strip().upper() for c in df.columns]

# --- Convert data types ---
df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"], errors="coerce")
df["QUANTITYORDERED"] = pd.to_numeric(df["QUANTITYORDERED"], errors="coerce").fillna(0).astype(int)
df["PRICEEACH"] = pd.to_numeric(df["PRICEEACH"], errors="coerce").fillna(0.0)

# --- Create total sales ---
df["TOTALSALES"] = df["QUANTITYORDERED"] * df["PRICEEACH"]

# --- Filter shipped orders only ---
df = df[df["STATUS"].str.lower() == "shipped"]

# --- Optional enhancements ---
# Capitalize and clean string columns
for col in ["COUNTRY", "CITY", "CUSTOMERNAME", "PRODUCTLINE", "DEALSIZE"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.title().str.strip()

# Fill nulls in key columns
df.fillna({
    "COUNTRY": "Unknown",
    "CITY": "Not Available",
    "PRODUCTLINE": "Unknown",
    "DEALSIZE": "Unknown"
}, inplace=True)

print(f"Cleaned data — {len(df)} shipped orders retained")

# ============================================================
# 5️⃣ Stage Clean Data
# ============================================================
stg_cols = [
    "ORDERNUMBER", "ORDERDATE", "PRODUCTCODE", "PRODUCTLINE",
    "CUSTOMERNAME", "COUNTRY", "CITY", "DEALSIZE",
    "QUANTITYORDERED", "PRICEEACH", "TOTALSALES"
]
df_stg = df[stg_cols].copy()
df_stg.to_sql("clean_sales", engine, schema="stg", if_exists="replace", index=False)
print("✅ Created staging table: stg.clean_sales")

# ============================================================
# 6️⃣ Create Dimension Tables
# ============================================================

# --- dim_customer ---
dim_customer = (
    df_stg[["CUSTOMERNAME", "COUNTRY", "CITY"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_customer["customer_key"] = dim_customer.index + 1
dim_customer.to_sql("dim_customer", engine, schema="analytics", if_exists="replace", index=False)

# --- dim_product ---
dim_product = (
    df_stg[["PRODUCTCODE", "PRODUCTLINE"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
dim_product["product_key"] = dim_product.index + 1
dim_product.to_sql("dim_product", engine, schema="analytics", if_exists="replace", index=False)

# --- dim_date (continuous, no gaps) ---
start_date = df_stg["ORDERDATE"].min().date()
end_date = df_stg["ORDERDATE"].max().date()
full_dates = pd.date_range(start_date, end_date, freq="D")

dim_date = pd.DataFrame({"ORDERDATE": full_dates})
dim_date["date_key"] = dim_date.index + 1
dim_date["year"] = dim_date["ORDERDATE"].dt.year
dim_date["month"] = dim_date["ORDERDATE"].dt.month
dim_date["day"] = dim_date["ORDERDATE"].dt.day
dim_date["month_name"] = dim_date["ORDERDATE"].dt.strftime("%B")
dim_date["quarter"] = dim_date["ORDERDATE"].dt.quarter
dim_date.to_sql("dim_date", engine, schema="analytics", if_exists="replace", index=False)

print("✅ Created dimension tables: dim_customer, dim_product, dim_date")

# ============================================================
# 7️⃣ Create Fact Table
# ============================================================
fact = (
    df_stg
    .merge(dim_customer, on=["CUSTOMERNAME", "COUNTRY", "CITY"], how="left")
    .merge(dim_product, on=["PRODUCTCODE", "PRODUCTLINE"], how="left")
    .merge(dim_date, on=["ORDERDATE"], how="left")
)

fact_sales = fact[[
    "ORDERNUMBER", "customer_key", "product_key", "date_key",
    "QUANTITYORDERED", "PRICEEACH", "TOTALSALES", "DEALSIZE"
]].copy()

fact_sales.rename(columns={"ORDERNUMBER": "sales_key"}, inplace=True)
fact_sales.to_sql("fact_sales", engine, schema="analytics", if_exists="replace", index=False)

print("✅ Created fact table: analytics.fact_sales")

# ============================================================
# 8️⃣ Create Indexes for Performance
# ============================================================
with engine.connect() as conn:
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_fact_sales_datekey ON analytics.fact_sales(date_key);"))
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_fact_sales_custkey ON analytics.fact_sales(customer_key);"))
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_fact_sales_prodkey ON analytics.fact_sales(product_key);"))
    conn.commit()
print("⚙️ Added performance indexes for Power BI queries")

# ============================================================
# 9️⃣ Completion Message
# ============================================================
print("\n🎯 Data Warehouse Build Complete (Enhanced Version)")
print("✅ Schemas: raw, stg, analytics")
print("✅ Tables and indexes created successfully in PostgreSQL")
print("✅ Ready for Power BI connection!")
