SELECT 
  f.fuel_type,
  COUNT(*) AS load_count,
  SUM(p.gallons_loaded) AS total_gallons,
  AVG(p.price_per_gallon) AS avg_price
FROM pump_loads p
JOIN fuels f ON f.fuel_type = p.fuel_type
GROUP BY f.fuel_type
ORDER BY total_gallons DESC;
