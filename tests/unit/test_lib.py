import pandas as pd

from lib import mask_secret, predict_fare, trips_query


def test_trips_query_limit():
    assert trips_query(10) == "select * from samples.nyctaxi.trips limit 10"


def test_predict_fare_mean():
    data = pd.DataFrame(
        {
            "pickup_zip": [10003, 10003, 11238],
            "dropoff_zip": [11238, 11238, 10003],
            "fare_amount": [10.0, 20.0, 99.0],
        }
    )
    assert predict_fare(data, 10003, 11238) == 15.0


def test_predict_fare_default_when_empty():
    data = pd.DataFrame({"pickup_zip": [1], "dropoff_zip": [2], "fare_amount": [5.0]})
    assert predict_fare(data, 10003, 11238) == 99.0


def test_mask_secret():
    assert mask_secret("abcd1234") == "****1234"
    assert mask_secret("") == "(missing)"
