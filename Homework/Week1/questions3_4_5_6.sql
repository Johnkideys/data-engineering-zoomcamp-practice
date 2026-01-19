-- SELECT COUNT(*) FROM public.green_taxi_data_nov_25;
-- SELECT COUNT(*) FROM public.taxi_zone;

SELECT * FROM public.green_taxi_data_nov_25 WHERE "RatecodeID" = 99 ; -- LIMIT 10
SELECT * FROM public.green_taxi_data_nov_25 WHERE trip_type = 1
SELECT * FROM public.green_taxi_data_nov_25 LIMIT 5
SELECT COUNT(*) FROM public.green_taxi_data_nov_25
SELECT COUNT (DISTINCT "RatecodeID") FROM green_taxi_data_nov_25

/*
3- For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' 
and '2025-12-01',  exclusive of the upper bound), how many trips had a 
trip_distance of less than or equal to 1 mile?
*/

SELECT COUNT(*)
FROM green_taxi_data_nov_25
WHERE lpep_pickup_datetime < '2025-12-01' 
AND lpep_pickup_datetime >= '2025-11-01'
AND trip_distance <= 1

-- SELECT * 
-- FROM green_taxi_data_nov_25
-- WHERE lpep_pickup_datetime >= '2025-11-01' 

/*
4- Which was the pick up day with the longest trip distance? 
Only consider trips with trip_distance less than 100 miles 
(to exclude data errors).
*/

SELECT 
DATE(lpep_pickup_datetime) as longest_trip_day,
trip_distance
FROM green_taxi_data_nov_25
WHERE trip_distance <= 100
ORDER BY trip_distance DESC
LIMIT 1

/*
5- Which was the pickup zone with the largest total_amount (sum of all trips) 
on November 18th, 2025?
*/

SELECT * FROM taxi_zone

SELECT 
	"PULocationID",
	"LocationID",
	ROUND(SUM(total_amount)::numeric, 1) as total_amount,
	"Borough", 
	"Zone"
FROM green_taxi_data_nov_25 g
LEFT JOIN taxi_zone t ON g."PULocationID" = t."LocationID"
WHERE DATE(lpep_pickup_datetime) = '2025-11-18'
GROUP BY "PULocationID", "LocationID", "Borough", "Zone"
ORDER BY total_amount DESC
LIMIT 1

/*
6- For the passengers picked up in the zone named "East Harlem North" 
in November 2025, which was the drop off zone that had the largest tip?
Note: it's tip , not trip. We need the name of the zone, not the ID.
*/

SELECT 
	t1."Zone",
	g.tip_amount
FROM green_taxi_data_nov_25 g
LEFT JOIN taxi_zone t1 ON g."DOLocationID" = t1."LocationID"
LEFT JOIN taxi_zone t2 ON g."PULocationID" = t2."LocationID"
WHERE lpep_pickup_datetime < '2025-12-01' -- Dont write DATE(lpep_pickup_datetime) <= '2025-11-30'
AND lpep_pickup_datetime >= '2025-11-01'
AND t2."Zone" = 'East Harlem North'
ORDER BY g.tip_amount DESC
LIMIT 1

-- SELECT *
-- FROM taxi_zone 
-- WHERE "LocationID" = 42


-- With window function (below is chatgpt solution when I asked for a better query)
SELECT
    dropoff_zone,
    tip_amount
FROM (
    SELECT
        tz_do."Zone" AS dropoff_zone,
        g.tip_amount,
        ROW_NUMBER() OVER (ORDER BY g.tip_amount DESC) AS rn
    FROM green_taxi_data_nov_25 g
    JOIN taxi_zone tz_pu
      ON g."PULocationID" = tz_pu."LocationID"
    JOIN taxi_zone tz_do
      ON g."DOLocationID" = tz_do."LocationID"
    WHERE tz_pu."Zone" = 'East Harlem North'
      AND g.lpep_pickup_datetime >= TIMESTAMP '2025-11-01'
      AND g.lpep_pickup_datetime <  TIMESTAMP '2025-12-01'
) x
WHERE rn = 1;




