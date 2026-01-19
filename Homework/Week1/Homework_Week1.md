# Module 1 Homework: Docker & SQL

## My Solution: Question 1
Below is the command to create the image:
`% docker run --rm --entrypoint bash python:3.13`
Checking pip version with:
Then inside the container we do: `pip --version` and this returns 
`pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)`

## My Solution: Question 2
Both of the below would work. Can use the service name or container name as the host. 
Note that the containers are on the same dopcker network by default as they are created from the docker-compose.yaml file (standard is the service name).
- db:5432
- postgres:5432
If I was connecting to the postgres container via pgadmin desktop(which would be on my local machine) I would then use localhost:5433.

## My Solution: Question 3,4,5,6
```
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
```
