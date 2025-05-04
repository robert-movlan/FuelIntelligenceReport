# 📘 Technical Diary — Fuel Intelligence Report

This document captures the **technical journey**, **challenges**, and **solutions** during the Fuel Intelligence Report build. It's intended for recruiters, collaborators, or certification reviewers to understand the depth of knowledge demonstrated in this project.

---

## 📅 Day 1–2: Setting Up the Environment

### ✅ Actions Taken:

* Created 4 source CSVs: `clients.csv`, `drivers.csv`, `fuels.csv`, `pump_loads.csv`
* Uploaded to Azure Data Lake Storage Gen2 (`fuelintelligencestorage` → `fueldata` container)

### ⚠️ Challenge:

Couldn’t validate the uploaded files directly through Synapse — needed preview.

### 💡 Solution:

Opened in Storage Explorer first, then validated using `OPENROWSET` SQL after transformation.

---

## 📅 Day 3: Azure Databricks Setup and Notebook Writing

### ✅ Actions Taken:

* Created cluster (`Standard_DS3_v2`)
* Authenticated Azure Data Lake Gen2 with App Registration

### ⚠️ Challenge:

Could not read from storage — error `403: This request is not authorized`

### 💡 Solution:

* Created an App Registration `FuelDatabricksAccess`
* Added `Storage Blob Data Contributor` role to the service principal
* Configured Spark with:

```python
spark.conf.set("fs.azure.account.auth.type...", "OAuth")
spark.conf.set("fs.azure.account.oauth2.client.id", "<client_id>")
... etc
```

* Used OAuth token endpoint for proper identity

---

## 📅 Day 4: Data Transformation in Notebook

### ✅ Data Joined and Written to:

* `/fueldata/final/fuel_report.parquet`

### 📄 Parquet Validation:

* Created `validate_parquet.sql`:

```sql
SELECT * FROM OPENROWSET(... FORMAT='PARQUET')
```

### ✅ Curated Outputs:

* `top_drivers.parquet`
* `fuel_cost_per_client.parquet`
* `fuel_type_usage.parquet`

---

## 📅 Day 5: Automating With Synapse + Pipelines

### ✅ Created:

* Azure Synapse pipeline `Refresh_FuelReport_Weekly`
* Used **Web Activity** to call **Databricks REST API**
* Scheduled with **Weekly Trigger**

### ⚠️ Challenge:

Couldn’t use direct Synapse → Databricks activity (incompatibility with runtime 15.4)

### 💡 Solution:

Used manual `POST` call to:

```
https://<workspace-url>/api/2.1/jobs/run-now
```

With bearer token from service principal

---

## 📷 Screenshots Captured for Evidence:

* ✅ `upload_to_datalake.png`
* ✅ `notebook_execution.png`
* ✅ `job_trigger_synapse.png`

---

## ✅ Summary of Outputs

* 1 Notebook: `1_ingest_to_datalake.ipynb`
* 4 SQLs in `/queries` folder
* 3 Curated Parquet files in `/curated/`
* Full working Synapse pipeline
* Real OAuth + Azure Role-based Access

---

## 📌 Next Steps

* Load curated Parquet files into Snowflake warehouse
* Continue Power Platform integrations:

  * Power Apps dashboards for executives
  * Power Automate flows for fuel alerts
  * Canva summaries for CEOs

---

## 👨‍💻 Author

**Movlan Aliyev**
GitHub: \[Your Profile] | Contact: [robert.movlan@outlook.com](mailto:robert.movlan@outlook.com)
