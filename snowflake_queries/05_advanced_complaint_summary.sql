WITH complaint_stats AS (
    SELECT
        complaint_state AS State,
        COUNT(*) AS TotalComplaints,
        COUNT_IF(status = 'Open') AS OpenComplaints,
        COUNT_IF(status = 'Closed') AS ClosedComplaints,
        ROUND(AVG(days_open), 1) AS AvgDaysOpen,
        MAX(days_open) AS MaxDaysOpen,
        MIN(complaint_created_on_date) AS EarliestComplaint,
        MAX(complaint_created_on_date) AS LatestComplaint
    FROM VW_CLEAN_COMPLAINTS
    GROUP BY complaint_state
),
latest_by_state AS (
    SELECT
        State,
        ComplaintId,
        Reason,
        CreatedDate,
        ROW_NUMBER() OVER (PARTITION BY State ORDER BY CreatedDate DESC) AS row_rank
    FROM VW_CLEAN_COMPLAINTS
)
SELECT
    cs.State,
    cs.TotalComplaints,
    cs.OpenComplaints,
    cs.ClosedComplaints,
    cs.AvgDaysOpen,
    cs.MaxDaysOpen,
    cs.EarliestComplaint,
    cs.LatestComplaint,
    lb.ComplaintId AS LatestComplaintID,
    lb.Reason AS LatestReason,
    lb.CreatedDate AS LatestCreatedDate
FROM complaint_stats cs
LEFT JOIN latest_by_state lb
  ON cs.State = lb.State AND lb.row_rank = 1
ORDER BY cs.TotalComplaints DESC;
