CREATE OR REPLACE VIEW VW_CLEAN_COMPLAINTS AS
SELECT
    complaint_number AS ComplaintId,
    complaint_created_on_date AS CreatedDate,
    complaint_closed_date AS ClosedDate,
    complaint_reason AS Reason,
    complaint_state AS State,
    status AS Status,
    days_open AS DaysOpen
FROM FUEL_DB.PUBLIC.Complaints;
