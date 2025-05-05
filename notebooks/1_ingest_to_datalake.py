# Databricks notebook source

# ✅ Load environment variables from .env file
from dotenv import load_dotenv
import os

load_dotenv()  # Automatically loads variables from .env

# ✅ Read secrets and parameters securely
storage_account_name = os.getenv("STORAGE_ACCOUNT_NAME")
container_name = os.getenv("CONTAINER_NAME")
mount_point = f"/mnt/{container_name}"

storage_account_key = os.getenv("AZURE_STORAGE_KEY")
client_secret = os.getenv("AZURE_CLIENT_SECRET")  # Optional if needed for other APIs

# ✅ Configure Spark to use the secure key
spark.conf.set(
    f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net",
    storage_account_key
)

# ✅ Mount the blob container to DBFS (Databricks File System)
dbutils.fs.mount(
    source = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/",
    mount_point = mount_point,
    extra_configs = {
        f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net": storage_account_key
    }
)



# COMMAND ----------

# Define the path once
base_path = "/mnt/fueldata"

# Read each CSV file
df_clients = spark.read.option("header", True).csv(f"{base_path}/clients.csv")
df_drivers = spark.read.option("header", True).csv(f"{base_path}/drivers.csv")
df_fuels = spark.read.option("header", True).csv(f"{base_path}/fuels.csv")
df_pump_loads = spark.read.option("header", True).csv(f"{base_path}/pump_loads.csv")

# Show top rows from each DataFrame
display(df_clients)
display(df_drivers)
display(df_fuels)
display(df_pump_loads)


# COMMAND ----------

df_clients.createOrReplaceTempView("clients")
df_drivers.createOrReplaceTempView("drivers")
df_fuels.createOrReplaceTempView("fuels")
df_pump_loads.createOrReplaceTempView("pump_loads")


# COMMAND ----------

SELECT 
  p.load_id,
  d.driver_id,
  d.name AS driver_name,
  d.license_n,
  d.experience_years,
  f.fuel_type,
  f.price_per_gallon,
  p.gallons,
  ROUND(p.gallons * f.price_per_gallon, 2) AS total_fuel_cost,
  c.client_id,
  c.name AS client_name,
  c.country,
  c.state,
  c.outstanding_amount,
  p.state_tax,
  p.excise_tax,
  p.note,
  p.timestamp
FROM pump_loads p
JOIN drivers d ON p.driver_id = d.driver_id
JOIN fuels f ON p.fuel_id = f.fuel_id
JOIN clients c ON p.client_id = c.client_id


# COMMAND ----------

fuel_report_df = spark.sql("""
SELECT 
  p.load_id,
  d.driver_id,
  d.name AS driver_name,
  d.license_n,
  d.experience_years,
  f.fuel_type,
  f.price_per_gallon,
  p.gallons,
  ROUND(p.gallons * f.price_per_gallon, 2) AS total_fuel_cost,
  c.client_id,
  c.name AS client_name,
  c.country,
  c.state,
  c.outstanding_amount,
  p.state_tax,
  p.excise_tax,
  p.note,
  p.timestamp
FROM pump_loads p
JOIN drivers d ON p.driver_id = d.driver_id
JOIN fuels f ON p.fuel_id = f.fuel_id
JOIN clients c ON p.client_id = c.client_id
""")

fuel_report_df.show(5, truncate=False)


# COMMAND ----------

fuel_report_df = spark.sql("""
SELECT 
  p.load_id,
  d.driver_id,
  d.name AS driver_name,
  d.license_number,
  d.experience_years,
  f.fuel_type,
  f.price_per_gallon,
  p.gallons,
  ROUND(p.gallons * f.price_per_gallon, 2) AS total_fuel_cost,
  c.client_id,
  c.name AS client_name,
  c.country,
  c.state,
  c.outstanding_amount,
  p.state_tax,
  p.excise_tax,
  p.note,
  p.timestamp
FROM pump_loads p
JOIN drivers d ON p.driver_id = d.driver_id
JOIN fuels f ON p.fuel_id = f.fuel_id
JOIN clients c ON p.client_id = c.client_id
""")

fuel_report_df.show(5, truncate=False)


# COMMAND ----------

spark.read.csv("/mnt/data/pump_loads.csv", header=True, inferSchema=True).printSchema()


# COMMAND ----------

fuel_report_df = spark.sql("""
SELECT 
  p.load_id,
  d.driver_id,
  d.name AS driver_name,
  d.license_number,
  d.experience_years,
  f.fuel_type,
  f.price_per_gallon,
  p.gallons_l,
  ROUND(p.gallons_l * f.price_per_gallon, 2) AS total_fuel_cost,
  c.client_id,
  c.name AS client_name,
  c.country,
  c.state,
  c.outstanding_amount,
  p.state_tax,
  p.excise_tax,
  p.note,
  p.timestamp
FROM pump_loads p
JOIN drivers d ON p.driver_id = d.driver_id
JOIN fuels f ON p.fuel_id = f.fuel_id
JOIN clients c ON p.client_id = c.client_id
""")

fuel_report_df.show(5, truncate=False)


# COMMAND ----------

fuel_report_df = spark.sql("""
SELECT 
  p.load_id,
  d.driver_id,
  d.name AS driver_name,
  d.license_number,
  d.experience_years,
  f.fuel_type,
  f.price_per_gallon,
  p.gallons_loaded,
  ROUND(p.gallons_loaded * f.price_per_gallon, 2) AS total_fuel_cost,
  c.client_id,
  c.name AS client_name,
  c.country,
  c.state,
  c.outstanding_amount,
  p.state_tax,
  p.excise_tax,
  p.note,
  p.timestamp
FROM pump_loads p
JOIN drivers d ON p.driver_id = d.driver_id
JOIN fuels f ON p.fuel_id = f.fuel_id
JOIN clients c ON p.client_id = c.client_id
""")

fuel_report_df.show(5, truncate=False)


# COMMAND ----------

# Define path to final output folder in Data Lake
final_path = f"/mnt/data/final/fuel_report.parquet"

# COMMAND ----------


# Save DataFrame as Parquet
fuel_report_df.write.mode("overwrite").parquet(final_path)

# COMMAND ----------

print("✅ fuel_report_df successfully written to Data Lake as Parquet.")


# COMMAND ----------

dbutils.fs.cp(
  "dbfs:/mnt/data/final/fuel_report.parquet",
  "dbfs:/mnt/fueldata/final/fuel_report.parquet",
  recurse=True
)


# COMMAND ----------

df.write.mode("overwrite").parquet("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/curated/top_drivers.parquet")


# COMMAND ----------

top_drivers_df = spark.sql("""
  SELECT 
    d.driver_id,
    d.name AS driver_name,
    SUM(p.gallons) AS total_gallons,
    COUNT(p.load_id) AS deliveries
  FROM pump_loads p
  JOIN drivers d ON p.driver_id = d.driver_id
  GROUP BY d.driver_id, d.name
  ORDER BY total_gallons DESC
  LIMIT 5
""")

top_drivers_df.write.mode("overwrite").parquet("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/curated/top_drivers.parquet")


# COMMAND ----------

# Load data from Data Lake
drivers = spark.read.option("header", True).csv("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/drivers.csv")
pump_loads = spark.read.option("header", True).csv("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/pump_loads.csv")

# COMMAND ----------

# Set OAuth config for accessing Azure Data Lake Gen2
spark.conf.set("fs.azure.account.auth.type.fuelintelligencestorage.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.fuelintelligencestorage.dfs.core.windows.net", 
               "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.fuelintelligencestorage.dfs.core.windows.net", 
               "42415ee4-49b0-4c60-bc55-7ebb8a6bcce5")
spark.conf.set("fs.azure.account.oauth2.client.secret.fuelintelligencestorage.dfs.core.windows.net", client_secret)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.fuelintelligencestorage.dfs.core.windows.net", 
               "https://login.microsoftonline.com/3ba40b32-cd04-4c04-950e-b9fdf6fc7d9e/oauth2/token")


# COMMAND ----------

# Validate connection to Azure Data Lake
df = spark.read.option("header", True).csv("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/drivers.csv")
display(df)


# COMMAND ----------

spark.conf.set("fs.azure.account.auth.type.fuelintelligencestorage.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.fuelintelligencestorage.dfs.core.windows.net", 
               "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.fuelintelligencestorage.dfs.core.windows.net", 
               "42415ee4-49b0-4c60-bc55-7ebb8a6bcce5")
spark.conf.set("fs.azure.account.oauth2.client.secret.fuelintelligencestorage.dfs.core.windows.net", client_secret)
spark.conf.set("fs.azure.account.oauth2.client.endpoint.fuelintelligencestorage.dfs.core.windows.net", 
               "https://login.microsoftonline.com/3ba40b32-cd04-4c04-950e-b9fdf6fc7d9e/oauth2/token")


# COMMAND ----------

df = spark.read.option("header", True).csv("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/drivers.csv")
df.show()


# COMMAND ----------

fuels = spark.read.option("header", True).csv("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/fuels.csv")
clients = spark.read.option("header", True).csv("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/clients.csv")
pump_loads = spark.read.option("header", True).csv("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/pump_loads.csv")


# COMMAND ----------

abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/curated/


# COMMAND ----------

top_drivers_df = spark.sql("""
SELECT 
    d.driver_id,
    d.name AS driver_name,
    SUM(p.gallons_loaded) AS total_gallons,
    COUNT(p.load_id) AS total_deliveries
FROM pump_loads p
JOIN drivers d ON d.driver_id = p.driver_id
GROUP BY d.driver_id, d.name
ORDER BY total_gallons DESC
LIMIT 5
""")

top_drivers_df.write.mode("overwrite").parquet("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/curated/top_5_drivers.parquet")


# COMMAND ----------

top_drivers_df = spark.sql("""
SELECT 
    d.driver_id,
    d.name AS driver_name,
    SUM(p.gallons_loaded) AS total_gallons,
    COUNT(p.load_id) AS total_deliveries
FROM pump_loads p
JOIN drivers d ON d.driver_id = p.driver_id
GROUP BY d.driver_id, d.name
ORDER BY total_gallons DESC
LIMIT 5
""")

top_drivers_df.write.mode("overwrite").parquet("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/curated/top_5_drivers.parquet")


# COMMAND ----------

# Load CSVs from Data Lake
drivers = spark.read.option("header", True).csv("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/drivers.csv")
pump_loads = spark.read.option("header", True).csv("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/pump_loads.csv")

# COMMAND ----------

# Register as temporary views
drivers.createOrReplaceTempView("drivers")
pump_loads.createOrReplaceTempView("pump_loads")

# COMMAND ----------

top_drivers_df = spark.sql("""
SELECT 
    d.driver_id,
    d.name AS driver_name,
    SUM(p.gallons_loaded) AS total_gallons,
    COUNT(p.load_id) AS total_deliveries
FROM pump_loads p
JOIN drivers d ON d.driver_id = p.driver_id
GROUP BY d.driver_id, d.name
ORDER BY total_gallons DESC
LIMIT 5
""")

top_drivers_df.write.mode("overwrite").parquet("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/curated/top_5_drivers.parquet")


# COMMAND ----------

fuel_cost_per_client = spark.sql("""
SELECT 
    c.client_id,
    c.name AS client_name,
    SUM(p.total_fuel_cost) AS total_spent,
    COUNT(p.load_id) AS total_deliveries
FROM pump_loads p
JOIN clients c ON c.client_id = p.client_id
GROUP BY c.client_id, c.name
ORDER BY total_spent DESC
""")

fuel_cost_per_client.write.mode("overwrite").parquet("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/curated/fuel_cost_per_client.parquet")


# COMMAND ----------

# Load CSVs
clients = spark.read.option("header", True).csv("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/clients.csv")
fuels = spark.read.option("header", True).csv("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/fuels.csv")

# COMMAND ----------

# Register as temp views
clients.createOrReplaceTempView("clients")
fuels.createOrReplaceTempView("fuels")

# COMMAND ----------

fuel_cost_per_client = spark.sql("""
SELECT 
    c.client_id,
    c.name AS client_name,
    SUM(p.gallons_loaded * f.price_per_gallon) AS total_spent,
    COUNT(p.load_id) AS total_deliveries
FROM pump_loads p
JOIN clients c ON c.client_id = p.client_id
JOIN fuels f ON f.fuel_id = p.fuel_id
GROUP BY c.client_id, c.name
ORDER BY total_spent DESC
""")

fuel_cost_per_client.write.mode("overwrite").parquet("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/curated/fuel_cost_per_client.parquet")


# COMMAND ----------

fuel_type_usage = spark.sql("""
SELECT 
    f.fuel_type,
    COUNT(*) AS load_count,
    SUM(p.gallons_loaded) AS total_gallons,
    AVG(f.price_per_gallon) AS avg_price
FROM pump_loads p
JOIN fuels f ON f.fuel_id = p.fuel_id
GROUP BY f.fuel_type
ORDER BY total_gallons DESC
""")

fuel_type_usage.write.mode("overwrite").parquet("abfss://fueldata@fuelintelligencestorage.dfs.core.windows.net/curated/fuel_type_usage.parquet")
