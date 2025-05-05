-- Total Complaints
SELECT COUNT(*) AS TotalComplaints FROM VW_CLEAN_COMPLAINTS;

-- Open Complaints
SELECT COUNT(*) AS OpenComplaints 
FROM VW_CLEAN_COMPLAINTS
WHERE Status = 'Open';

-- Average Days Open (for Closed)
SELECT ROUND(AVG(DaysOpen), 2) AS AvgDaysOpen
FROM VW_CLEAN_COMPLAINTS
WHERE Status = 'Closed';
