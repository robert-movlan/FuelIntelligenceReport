# 📊 Fuel Intelligence Report — GitHub Portfolio Documentation

## 🔍 Project Overview

This project showcases a full end-to-end data integration solution for a fictional fuel logistics company. The architecture integrates:

* Azure Data Lake Storage Gen2
* Azure Databricks (for processing & transformation)
* Azure Synapse Analytics (for querying and automation)
* Azure Data Factory (for orchestration)

Future phases will include:

* Snowflake integration
* Power Apps for executive dashboards
* Power Automate for alerts
* Canva/Power BI visuals for stakeholders

---

## ✅ Current Status (Phase 1 Completed)

### 🔸 Data Ingestion:

* ✅ 4 CSV files uploaded to Azure Data Lake under container `fueldata`

  * `clients.csv`
  * `drivers.csv`
  * `fuels.csv`
  * `pump_loads.csv`

### 🔸 Databricks Processing:

* ✅ Created cluster: `Movlan Aliyev’s Cluster`
* ✅ Notebook `1_ingest_to_datalake.ipynb` performs the following:

  * Joins 4 datasets
  * Cleans and prepares the final data
  * Writes to: `/fueldata/final/fuel_report.parquet`
  * Generates 3 curated parquet files:

    * `/curated/top_drivers.parquet`
    * `/curated/fuel_cost_per_client.parquet`
    * `/curated/fuel_type_usage.parquet`

### 🔸 Weekly Automation:

* ✅ Created Databricks Job to run notebook
* ✅ Triggered via Azure Synapse Pipeline with Web Activity using REST API
* ✅ Scheduled weekly recurrence trigger using Synapse

### 🔸 Validation:

* ✅ Successfully queried `fuel_report.parquet` in Synapse using `OPENROWSET`
* ✅ Created 4 SQL scripts:

  * `validate_parquet.sql`
  * `top_drivers.sql`
  * `fuel_cost_per_client.sql`
  * `fuel_type_usage.sql`
* ✅ Screenshots saved for each pipeline, job, and notebook run

---

## ⚠️ Obstacles Faced & How They Were Resolved

| Issue                                                       | Solution                                                                                               |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Databricks runtime version 15.4 not compatible with Synapse | Changed to Runtime 13.3 LTS                                                                            |
| Spark job failing with 9512 error                           | Manually created Databricks Job and triggered via Synapse Web activity instead of direct notebook link |
| Could not locate `fuel_report.parquet`                      | Found it was in `/fueldata/final/` not `/fueldata/`                                                    |
| Encoding errors for VARCHAR fields                          | Will handle using UTF-8 collation hint in downstream SQL queries                                       |
| Storage credential issues                                   | Fixed by registering App in Azure AD and assigning Storage Blob Data Contributor role                  |

---

## 📁 Folder Structure

```
/Fuel_Intelligence_Report
│
├── data/
│   ├── clients.csv
│   ├── drivers.csv
│   ├── fuels.csv
│   └── pump_loads.csv
│
├── notebooks/
│   └── 1_ingest_to_datalake.ipynb
│
├── pipelines/
│   └── Refresh_FuelReport_Weekly_support_live/ (exported Synapse pipeline)
│
├── queries/
│   ├── validate_parquet.sql
│   ├── top_drivers.sql
│   ├── fuel_cost_per_client.sql
│   └── fuel_type_usage.sql
│
├── screenshots/
│   ├── upload_to_datalake.png
│   ├── notebook_execution.png
│   └── job_trigger_synapse.png
│
├── readme_docs/
│   └── Technical_Diary.md 
│
└── README.md (this file)
```

---

## 🔗 Next Steps

* [ ] Create curated Synapse views with aggregations
* [ ] Load `fuel_report.parquet` into Snowflake
* [ ] Build Power Apps for CEO
* [ ] Automate reporting with Power Automate + Canva

---

## 👨‍💻 Author

**Movlan Aliyev** — \[[robert.movlan@outlook.com](mailto:robert.movlan@outlook.com)]
GitHub Portfolio: \[Coming Soon]

---

👉 For full technical documentation, visit: [`readme_docs/Technical_Diary.md`](./readme_docs/Technical_Diary.md)
