import pandas as pd
import numpy as np
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

bike_model = joblib.load(
    BASE_DIR / "Bicycle_Demand/model_compressed.pkl"
)

traffic_model = joblib.load(
    BASE_DIR / "Traffic_Volume/traffic_model_compressed.pkl"
)

traffic_prep = joblib.load(
    BASE_DIR / "Traffic_Volume/traffic_preprocessing.pkl"
)

subway_model = joblib.load(
    BASE_DIR / "Subway_Demand/subway_model_tuned_compressed.pkl"
)

subway_prep = joblib.load(
    BASE_DIR / "Subway_Demand/subway_preprocessing.pkl"
)

bike_station_model = joblib.load(
    BASE_DIR / "Bike_Station_Availability/bike_station_model_tuned_compressed.pkl"
)

bike_station_prep = joblib.load(
    BASE_DIR / "Bike_Station_Availability/bike_station_lag_preprocessing.pkl"
)

print("All four models loaded successfully!")
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# ==========================================
# 1. LOAD ALL MODELS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

bike_model = joblib.load(
    BASE_DIR / "Bicycle_Demand/model_compressed.pkl"
)

traffic_model = joblib.load(
    BASE_DIR / "Traffic_Volume/traffic_model_compressed.pkl"
)

traffic_prep = joblib.load(
    BASE_DIR / "Traffic_Volume/traffic_preprocessing.pkl"
)

subway_model = joblib.load(
    BASE_DIR / "Subway_Demand/subway_model_tuned_compressed.pkl"
)

subway_prep = joblib.load(
    BASE_DIR / "Subway_Demand/subway_preprocessing.pkl"
)

bike_station_model = joblib.load(
    BASE_DIR / "Bike_Station_Availability/bike_station_model_tuned_compressed.pkl"
)

bike_station_prep = joblib.load(
    BASE_DIR / "Bike_Station_Availability/bike_station_lag_preprocessing.pkl"
)

print("All four models loaded successfully!")


# ==========================================
# 2. COMMON INPUT FEATURES
# ==========================================

def common_features(date_time):

    dt = pd.Timestamp(date_time)

    return {
        "hour": dt.hour,
        "day": dt.day,
        "month": dt.month,
        "year": dt.year,
        "weekday": dt.weekday(),
        "is_weekend": int(dt.weekday() >= 5),
        "season": (dt.month % 12) // 3,
        "is_rush_hour": int(
            7 <= dt.hour <= 9 or
            16 <= dt.hour <= 19
        )
    }


# ==========================================
# 3. BICYCLE RENTAL DEMAND
# ==========================================

def predict_bicycle(
    date_time,
    season,
    holiday,
    weathersit,
    temp,
    atemp,
    hum,
    windspeed
):

    dt = pd.Timestamp(date_time)

    if dt.year not in [2011, 2012]:
        raise ValueError(
            "Select 2011 or 2012 for historical bicycle predictions."
        )

    inputs = {
        "season": season,
        "yr": dt.year - 2011,
        "mnth": dt.month,
        "hr": dt.hour,
        "holiday": holiday,
        "weekday": (dt.weekday() + 1) % 7,
        "workingday": int(
            dt.weekday() < 5 and holiday == 0
        ),
        "weathersit": weathersit,
        "temp": temp,
        "atemp": atemp,
        "hum": hum,
        "windspeed": windspeed
    }

    df = pd.DataFrame([inputs])

    if hasattr(bike_model, "feature_names_in_"):
        df = df[list(bike_model.feature_names_in_)]

    prediction = bike_model.predict(df)[0]

    return round(float(max(0, prediction)), 2)


# ==========================================
# 4. TRAFFIC VOLUME
# ==========================================

def predict_traffic(
    date_time,
    temp_celsius,
    rain_1h,
    snow_1h,
    clouds_all,
    weather_main,
    is_holiday
):

    inputs = common_features(date_time)

    inputs.update({
        "temp_celsius": temp_celsius,
        "rain_1h": rain_1h,
        "snow_1h": snow_1h,
        "clouds_all": clouds_all,
        "weather_main": weather_main,
        "is_holiday": is_holiday
    })

    df = pd.DataFrame([inputs])

    df = df[traffic_prep["feature_columns"]]

    if f"weather_main_{weather_main}" not in traffic_prep["encoded_columns"]:
        raise ValueError("Invalid weather category.")

    df = pd.get_dummies(
        df,
        columns=["weather_main"],
        dtype=int
    )

    df = df.reindex(
        columns=traffic_prep["encoded_columns"],
        fill_value=0
    )

    prediction = traffic_model.predict(df)[0]

    return round(float(max(0, prediction)), 2)


# ==========================================
# 5. SUBWAY PASSENGER DEMAND
# ==========================================

def predict_subway(
    date_time,
    station_id,
    latitude,
    longitude
):

    inputs = common_features(date_time)

    mapping = subway_prep["station_mapping"]

    station_id = str(station_id)

    if station_id not in mapping:
        raise ValueError("Invalid Subway Station ID")

    inputs.update({
        "station_code": mapping[station_id],
        "latitude": latitude,
        "longitude": longitude
    })

    df = pd.DataFrame([inputs])

    df = df[subway_prep["features"]]

    prediction = subway_model.predict(df)[0]

    return round(float(max(0, prediction)), 2)


# ==========================================
# 6. BIKE STATION AVAILABILITY
# ==========================================

def predict_bike_station(
    date_time,
    station_id,
    dock_count,
    lag_1h
):

    inputs = common_features(date_time)

    mapping = bike_station_prep["station_mapping"]

    station_id = str(station_id)

    if station_id not in mapping:
        raise ValueError("Invalid Bike Station ID")

    if dock_count <= 0:
        raise ValueError("Dock capacity must be positive.")

    if not 0 <= lag_1h <= dock_count:
        raise ValueError("Invalid previous-hour availability.")

    inputs.update({
        "station_code": mapping[station_id],
        "dock_count": dock_count,
        "lag_1h": lag_1h
    })

    df = pd.DataFrame([inputs])

    df = df[bike_station_prep["features"]]

    prediction = bike_station_model.predict(df)[0]

    prediction = np.clip(
        prediction,
        0,
        dock_count
    )

    return round(float(prediction), 2)