/*
  Model for DSP reports data
  This model reads from MongoDB and adds time dimensions and metrics
*/

SELECT
  campaign_id,
  impressions,
  revenue,
  cpm,
  revenue_per_impression,
  date,
  EXTRACT(YEAR FROM date) AS year,
  EXTRACT(MONTH FROM date) AS month,
  EXTRACT(DAY FROM date) AS day,
  EXTRACT(DOW FROM date) AS day_of_week,
  -- Calculate additional metrics
  (revenue / impressions) * 1000 AS calculated_cpm,
  CASE 
    WHEN cpm >= 10 THEN 'High'
    WHEN cpm >= 7 THEN 'Medium'
    ELSE 'Low'
  END AS cpm_tier
FROM 
  ${ref('mongodb')}
WHERE
  -- Only include records from the last 90 days
  date >= CURRENT_DATE - INTERVAL 90 DAY 