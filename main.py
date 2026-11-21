from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from allocation import (
    allocate_bicycles,
    allocate_traffic,
    allocate_subway,
    allocate_bike_station
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from predict import (
    predict_bicycle,
    predict_traffic,
    predict_subway,
    predict_bike_station
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)
app = FastAPI(
    title="Smart Mobility Forecasting System",
    version="1.0"
)
BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    return FileResponse(
        BASE_DIR / "templates" / "index.html"
    )


@app.get("/health")
def health():
    return {
        "message": "Smart Mobility API is running",
        "models": 4,
        "status": "Active"
    }


# Bicycle rental demand
@app.post("/predict/bicycle")
def bicycle(data: dict):
    try:
        result = predict_bicycle(**data)

        return {
            "model": "Bicycle Rental Demand",
            "prediction": result,
            "unit": "rentals per hour"
        }

    except (ValueError, TypeError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))


# Traffic volume
@app.post("/predict/traffic")
def traffic(data: dict):
    try:
        result = predict_traffic(**data)

        return {
            "model": "Traffic Volume",
            "prediction": result,
            "unit": "vehicles per hour"
        }

    except (ValueError, TypeError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))


# Subway passenger demand
@app.post("/predict/subway")
def subway(data: dict):
    try:
        result = predict_subway(**data)

        return {
            "model": "Subway Passenger Demand",
            "prediction": result,
            "unit": "passengers per hour"
        }

    except (ValueError, TypeError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))


# Bike station availability
@app.post("/predict/bike-station")
def bike_station(data: dict):
    try:
        result = predict_bike_station(**data)

        return {
            "model": "Bike Station Availability",
            "prediction": result,
            "unit": "available bicycles"
        }

    except (ValueError, TypeError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))


# Combined prediction endpoint
@app.post("/predict/all")
def predict_all(data: dict):
    try:
        return {
            "bicycle_demand": predict_bicycle(
                **data["bicycle"]
            ),
            "traffic_volume": predict_traffic(
                **data["traffic"]
            ),
            "subway_demand": predict_subway(
                **data["subway"]
            ),
            "bike_availability": predict_bike_station(
                **data["bike_station"]
            )
        }

    except (ValueError, TypeError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    