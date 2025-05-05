# Fuel Intelligence Report — GitHub Portfolio Documentation

## Project Overview

This project showcases a full end-to-end data integration and reporting solution for a fictional fuel logistics company. The architecture integrates:

- Azure Data Lake Storage Gen2  
- Azure Databricks (processing and transformation)  
- Azure Synapse Analytics (querying and automation)  
- Azure Data Factory (orchestration)  
- Snowflake (data warehousing and analysis)  
- Retool (executive dashboard interface)

Future phases will include:

- Power Apps for director/CEO-level dashboards  
- Power Automate for automated alerts and email triggers  
- Canva or Power BI for stakeholder-facing visuals

---

## Current Status (Phase 1 Completed)

### Data Ingestion

- 4 CSV files uploaded to Azure Data Lake under container `fueldata`:
  - `clients.csv`
  - `drivers.csv`
  - `fuels.csv`
  - `pump_loads.csv`

### Databricks Processing

- Created cluster: `Movlan Aliyev’s Cluster`
- Notebook `1_ingest_to_datalake.ipynb` performs the following:
  - Joins and cleans all 4 datasets
  - Outputs to `/fueldata/final/fuel_report.parquet`
  - Generates curated datasets:
    - `/curated/top_drivers.parquet`
    - `/curated/fuel_cost_per_client.parquet`
    - `/curated/fuel_type_usage.parquet`

### Weekly Automation

- Created Databricks Job to run notebook  
- Triggered using Azure Synapse Pipeline via Web Activity (Databricks REST API)  
- Weekly recurrence trigger set inside Synapse pipeline  

### Snowflake Integration

- Table created: `FUEL_DB.PUBLIC.COMPLAINTS`
- Loaded `complaints.csv` using Web UI file loader  
- 4 additional SQL scripts created and organized:
  - `01_create_table.sql`
  - `02_insert_sample_data.sql`
  - `03_create_view_clean.sql`
  - `04_kpi_queries.sql`
  - `05_advanced_complaint_summary.sql` (complex query for dashboards)

### Retool Dashboard (Live)

- Retool URL: [Fuel Intelligence Dashboard](https://aliyevm.retool.com/apps/eea905a4-299d-11f0-952f-e37a8dc5f852/Fuel%20Intelligence%20Dashboard/page1)
- Live integration with Snowflake using resource connector  
- Displays complaint table with fields like:
  - Complaint ID, State, Status, Reason, Days Open
- Ready for future enhancements: filters, charts, KPIs

---

## Obstacles Faced and Solutions

| Issue                                                       | Solution                                                                                               |
| ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Databricks runtime 15.4 not compatible with Synapse         | Downgraded to Runtime 13.3 LTS                                                                           |
| Spark job failed with 9512 error                            | Used manual Databricks Job and triggered via Synapse REST API instead of direct link                    |
| `fuel_report.parquet` not found                             | Corrected path from `/fueldata/` to `/fueldata/final/`                                                  |
| Retool failed to connect to Snowflake initially             | Fixed connector settings and workspace token                                                             |
| Power Apps access denied                                    | Switched to Retool for now to accelerate dashboard progress                                              |

---

## Folder Structure

/Fuel_Intelligence_Report
│
├── data/
│ ├── clients.csv
│ ├── drivers.csv
│ ├── fuels.csv
│ └── pump_loads.csv
│
├── notebooks/
│ └── 1_ingest_to_datalake.ipynb
│
├── pipelines/
│ └── Refresh_FuelReport_Weekly_support_live/
│
├── snowflake_queries/
│ ├── 01_create_table.sql
│ ├── 02_insert_sample_data.sql
│ ├── 03_create_view_clean.sql
│ ├── 04_kpi_queries.sql
│ └── 05_advanced_complaint_summary.sql
│
├── retool_dashboard/
│ ├── query_snowflake.sql
│ ├── README.md
│ └── screenshots/
│ └── table_view_simple.png
│
├── queries/
│ ├── validate_parquet.sql
│ ├── top_drivers.sql
│ ├── fuel_cost_per_client.sql
│ └── fuel_type_usage.sql
│
├── readme_docs/
│ └── Technical_Diary.md
│
└── README.md

yaml
Copy
Edit

---

## Next Steps

- [ ] Add filters and dynamic visualizations to Retool  
- [ ] Load processed `fuel_report.parquet` into Snowflake  
- [ ] Build director dashboard in Power Apps (alternative to Retool)  
- [ ] Trigger email alerts via Power Automate  
- [ ] Design a Canva summary page for business reviews  

---

## Author

**Movlan Aliyev**  
Email: robert.movlan@outlook.com  
GitHub Portfolio: [Coming Soon]

Full logs and documentation can be found in `readme_docs/Technical_Diary.md`