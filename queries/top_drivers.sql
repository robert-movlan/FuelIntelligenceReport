SELECT
  d.driver_id,
  d.name AS driver_name,
  SUM(p.gallons_loaded) AS total_gallons,
  COUNT(p.load_id) AS total_deliveries
FROM pump_loads p
JOIN drivers d ON p.driver_id = d.driver_id
GROUP BY d.driver_id, d.name
ORDER BY total_gallons DESC
LIMIT 5;
