-- validate_parquet.sql
SELECT * 
FROM OPENROWSET(
    BULK 'https://fuelintelligencestorage.dfs.core.windows.net/fueldata/final/fuel_report.parquet',
    FORMAT='PARQUET'
) AS [result];
