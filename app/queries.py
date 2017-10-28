import sqlalchemy

def get_engine():
    return sqlalchemy.create_engine("sqlite:///app/sample_trips.db")

_comparables_query = """
WITH closest_trips (fare_amount, tip_amt) AS (
    SELECT fare_amount, tip_amt
    FROM trips
    ORDER BY abs(pickup_latitude-({pickup_latitude})) + abs(pickup_longitude-({pickup_longitude})) +
        abs(dropoff_latitude-({dropoff_latitude})) + abs(dropoff_longitude-({dropoff_longitude}))
    LIMIT 20
)
SELECT AVG(fare_amount) AS fare_amount, AVG(tip_amt) AS tip_amt
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

