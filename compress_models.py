import joblib
import os

files = [
    "Bicycle_Demand/model.pkl",
    "Traffic_Volume/traffic_model.pkl",
    "Subway_Demand/subway_model_tuned.pkl",
    "Bike_Station_Availability/bike_station_model_tuned.pkl"
]

for path in files:

    print("\nCompressing:", path)

    model = joblib.load(path)

    new_path = path.replace(".pkl", "_compressed.pkl")

    joblib.dump(model, new_path, compress=3)

    old_size = os.path.getsize(path) / (1024 ** 2)
    new_size = os.path.getsize(new_path) / (1024 ** 2)

    print("Original size:", round(old_size, 2), "MB")
    print("Compressed size:", round(new_size, 2), "MB")

    del model

print("\nALL MODELS COMPRESSED SUCCESSFULLY!")