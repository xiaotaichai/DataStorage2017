import sqlalchemy

def get_engine():
    return sqlalchemy.create_engine("postgresql://Lydia@localhost:5432/taxi")

_get_lat_lng_bounds = """
SELECT LEAST(MIN(pick_lat),MIN(drop_lat)) AS min_lat,
       GREATEST(MAX(pick_lat),MAX(drop_lat)) AS max_lat,
       LEAST(MIN(pick_lng),MIN(drop_lng)) AS min_lng,
       GREATEST(MAX(pick_lng),MAX(drop_lng)) AS max_lng
       FROM std_fare
"""

def get_bounds():
    sql_engine = get_engine()
    sql_connection = sql_engine.connect()
    result = sql_connection.execute(_get_lat_lng_bounds)
    lat_min, lat_max, long_min, long_max = result.fetchone()
    result.close()
    return(lat_min, lat_max, long_min, long_max)

_comparables_query = """
WITH closest_trips (fare_amt, tip_amt, fees_amt) AS (
    SELECT fare, tip, tolls_fees
    FROM std_fare
    ORDER BY abs(pick_lat-({pickup_latitude})) + abs(pick_lng-({pickup_longitude})) +
        abs(drop_lat-({dropoff_latitude})) + abs(drop_lng-({dropoff_longitude}))
    LIMIT 20
)
SELECT AVG(fare_amt) AS fare_amt, AVG(tip_amt) AS tip_amt, AVG(fees_amt) AS fees_amt
FROM closest_trips
"""

def generate_comparables_query(from_lat, from_long, to_lat, to_long):
    return _comparables_query.format(pickup_latitude=from_lat,
                                     pickup_longitude=from_long,
                                     dropoff_latitude=to_lat,
                                     dropoff_longitude=to_long)

if __name__ == '__main__':
    from_lat, from_long = 40.711626, -73.959968
    to_lat, to_long = 40.671698, -73.978996
    engine = get_engine()
    conn = engine.connect()
    result = conn.execute(generate_comparables_query(from_lat, from_long, to_lat, to_long))
    print(result.fetchone())
    result.close()
