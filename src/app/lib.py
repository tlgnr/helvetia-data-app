"""Pure helpers so unit tests do not need Databricks or Streamlit."""


def trips_query(limit: int = 5000) -> str:
    if limit < 1:
        raise ValueError("limit must be >= 1")
    return f"select * from samples.nyctaxi.trips limit {int(limit)}"


def predict_fare(data, pickup_zip: int, dropoff_zip: int, default: float = 99.0) -> float:
    subset = data[(data["pickup_zip"] == pickup_zip) & (data["dropoff_zip"] == dropoff_zip)]
    if len(subset) == 0:
        return default
    return float(subset["fare_amount"].mean())


def mask_secret(value: str, visible: int = 4) -> str:
    if not value:
        return "(missing)"
    if len(value) <= visible:
        return "*" * len(value)
    return "*" * (len(value) - visible) + value[-visible:]
