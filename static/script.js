// =========================================
// SMART MOBILITY DASHBOARD
// Automatic predictions - no user inputs
// =========================================


// Historical demonstration inputs.
// These will be replaced by MySQL-backed
// automatic record selection later.

const DEMO_DATA = {

    bicycle: {
        date_time: "2012-06-15 08:00:00",
        season: 2,
        holiday: 0,
        weathersit: 1,
        temp: 0.65,
        atemp: 0.62,
        hum: 0.55,
        windspeed: 0.2
    },

    traffic: {
        date_time: "2018-06-15 08:00:00",
        temp_celsius: 25,
        rain_1h: 0,
        snow_1h: 0,
        clouds_all: 20,
        weather_main: "Clear",
        is_holiday: 0
    },

    subway: {
        date_time: "2024-06-15 08:00:00",
        station_id: "1",
        latitude: 40.775036,
        longitude: -73.912030
    },

    bike_station: {
        date_time: "2015-06-15 08:00:00",
        station_id: "2",
        dock_count: 20,
        lag_1h: 8
    },

    capacity: {
        rental_capacity: 500,
        road_capacity: 6000,
        capacity_per_train: 100,
        current_trains: 2
    }

};


// =========================================
// HELPER FUNCTIONS
// =========================================

function setText(id, value) {
    const element = document.getElementById(id);

    if (element) {
        element.textContent = value;
    }
}


function formatNumber(value) {
    return Number(value).toLocaleString(
        undefined,
        { maximumFractionDigits: 2 }
    );
}


function updateProgress(id, percentage) {

    const element = document.getElementById(id);

    if (!element) return;

    const value = Number(percentage);

    if (!Number.isFinite(value)) return;

    // Progress bar can only visually reach 100%.
    // Exact percentage is still shown separately.
    element.style.width = Math.min(
        Math.max(value, 0),
        100
    ) + "%";
}


function updateStatus(message, online) {

    setText("systemStatus", message);

    const container = document.querySelector(".system-status");

    if (container) {
        container.classList.toggle("online", online);
        container.classList.toggle("offline", !online);
    }
}


// =========================================
// UPDATE PREDICTION CARDS
// =========================================

function updatePredictions(data) {

    const bicycle = data.bicycle;
    const traffic = data.traffic;
    const subway = data.subway;
    const station = data.bike_station;

    // Bicycle
    setText(
        "bicyclePrediction",
        formatNumber(bicycle.predicted_demand)
    );

    setText("bicycleStatus", bicycle.status);


    // Traffic
    setText(
        "trafficPrediction",
        formatNumber(traffic.predicted_volume)
    );

    setText("trafficStatus", traffic.status);


    // Subway
    setText(
        "subwayPrediction",
        formatNumber(subway.predicted_passengers)
    );

    setText("subwayStatus", subway.status);


    // Bike station
    setText(
        "stationPrediction",
        formatNumber(station.predicted_available)
    );

    setText("stationStatus", station.status);
}


// =========================================
// UPDATE CAPACITY ANALYSIS
// =========================================

function updateCapacity(data) {

    const bicycle = data.bicycle.utilization_percent;
    const traffic = data.traffic.utilization_percent;

    const subwayCapacity =
        DEMO_DATA.capacity.capacity_per_train *
        DEMO_DATA.capacity.current_trains;

    const subway = subwayCapacity > 0
        ? (data.subway.predicted_passengers / subwayCapacity) * 100
        : null;

    const station = data.bike_station.occupancy_percent;


    setText(
        "bicycleUtilization",
        formatNumber(bicycle) + "%"
    );

    setText(
        "trafficUtilization",
        formatNumber(traffic) + "%"
    );

    setText(
        "subwayUtilization",
        subway === null
            ? "No scheduled capacity"
            : formatNumber(subway) + "%"
    );

    setText(
        "stationUtilization",
        formatNumber(station) + "%"
    );


    updateProgress("bicycleProgress", bicycle);
    updateProgress("trafficProgress", traffic);

    if (subway !== null) {
        updateProgress("subwayProgress", subway);
    }

    updateProgress("stationProgress", station);
}


// =========================================
// UPDATE RECOMMENDATIONS
// =========================================

function updateRecommendations(data) {

    const bicycle = data.bicycle;
    const traffic = data.traffic;
    const subway = data.subway;
    const station = data.bike_station;


    setText(
        "bicycleRecommendation",
        bicycle.recommendation +
        ". Additional hourly rental capacity required: " +
        bicycle.additional_rental_capacity
    );


    setText(
        "trafficRecommendation",
        traffic.recommendation +
        ". Road capacity utilization: " +
        formatNumber(traffic.utilization_percent) +
        "%."
    );


    setText(
        "subwayRecommendation",
        subway.recommendation +
        ". Additional train services estimated: " +
        subway.additional_trains
    );


    setText(
        "stationRecommendation",
        station.recommendation +
        ". Bikes to add: " +
        station.add_bikes +
        ". Bikes to remove: " +
        station.remove_bikes
    );
}


// =========================================
// FETCH RESULTS FROM FASTAPI
// =========================================

async function loadDashboard() {

    const errorBox = document.getElementById("errorMessage");

    if (errorBox) {
        errorBox.hidden = true;
    }

    try {

        const response = await fetch("/recommend/all", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(DEMO_DATA)

        });


        if (!response.ok) {

            const errorData = await response.json().catch(() => ({}));

            throw new Error(
                errorData.detail
                    ? JSON.stringify(errorData.detail)
                    : "API returned status " + response.status
            );

        }


        const results = await response.json();

        updatePredictions(results);
        updateCapacity(results);
        updateRecommendations(results);

        updateStatus("Models Connected", true);

        console.log("Smart Mobility Results:", results);

    } catch (error) {

        console.error("Dashboard Error:", error);

        updateStatus("Prediction Error", false);

        if (errorBox) {
            errorBox.textContent =
                "Unable to load predictions: " + error.message;

            errorBox.hidden = false;
        }

    }
}


// =========================================
// AUTOMATICALLY LOAD THE DASHBOARD
// =========================================

document.addEventListener("DOMContentLoaded", loadDashboard);