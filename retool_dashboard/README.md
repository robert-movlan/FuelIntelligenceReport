# 🚀 Retool Fuel Intelligence Dashboard

This dashboard shows live complaint data from Snowflake using a simple table view.

### 🔗 Live App
👉 [Open Retool Dashboard](https://aliyevm.retool.com/apps/eea905a4-299d-11f0-952f-e37a8dc5f852/Fuel%20Intelligence%20Dashboard/page1)

### 📄 Current View
A simple table listing complaint records with the following fields:
- Complaint ID
- Created Date
- Closed Date
- Reason
- State
- Status
- Days Open

### 🧠 Data Source
Data is pulled from the Snowflake view:
```sql
SELECT * FROM VW_CLEAN_COMPLAINTS ORDER BY CreatedDate DESC;
📸 Screenshot

🛠️ Coming Soon
Dropdown filters for status and state

KPI cards (Total complaints, Open complaints, Avg Days Open)

Interactive visual charts