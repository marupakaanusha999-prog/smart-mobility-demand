import math


# 1. Bicycle Rental Capacity Allocation

def allocate_bicycles(demand, rental_capacity):

    if demand < 0 or rental_capacity <= 0:
        raise ValueError("Invalid demand or capacity")

    additional_bikes = math.ceil(
        max(0, demand - rental_capacity)
    )

    utilization = demand / rental_capacity * 100

    if utilization > 100:
        status = "Insufficient Capacity"
        recommendation = "Increase bicycle rental capacity"

    elif utilization >= 80:
        status = "High Demand"
        recommendation = "Prepare additional bicycles"

    else:
        status = "Normal"
        recommendation = "Maintain current capacity"

    return {
        "predicted_demand": demand,
        "current_capacity": rental_capacity,
        "additional_rental_capacity": additional_bikes,
        "utilization_percent": round(utilization, 2),
        "status": status,
        "recommendation": recommendation
    }


# 2. Traffic Capacity Analysis

def allocate_traffic(volume, road_capacity):

    if volume < 0 or road_capacity <= 0:
        raise ValueError("Invalid volume or capacity")

    ratio = volume / road_capacity

    if ratio >= 1:
        status = "Critical"
        recommendation = "Review congestion management measures"

    elif ratio >= 0.8:
        status = "High Traffic"
        recommendation = "Monitor traffic and review signal timings"

    elif ratio >= 0.5:
        status = "Moderate Traffic"
        recommendation = "Continue traffic monitoring"

    else:
        status = "Low Traffic"
        recommendation = "Maintain normal operations"

    return {
        "predicted_volume": volume,
        "road_capacity": road_capacity,
        "utilization_percent": round(ratio * 100, 2),
        "status": status,
        "recommendation": recommendation
    }


# 3. Subway Capacity Allocation

def allocate_subway(
    demand,
    capacity_per_train,
    current_trains
):

    if demand < 0 or capacity_per_train <= 0 or current_trains < 0:
        raise ValueError("Invalid subway capacity inputs")

    required_trains = math.ceil(
        demand / capacity_per_train
    )

    additional_trains = max(
        0, required_trains - current_trains
    )

    if additional_trains > 0:
        status = "Insufficient Capacity"
        recommendation = "Review need for additional train services"

    else:
        status = "Sufficient Capacity"
        recommendation = "Maintain current service"

    return {
        "predicted_passengers": demand,
        "required_trains": required_trains,
        "current_trains": current_trains,
        "additional_trains": additional_trains,
        "status": status,
        "recommendation": recommendation
    }


# 4. Bike Station Rebalancing

def allocate_bike_station(available, dock_count):

    if dock_count <= 0 or not 0 <= available <= dock_count:
        raise ValueError("Invalid station availability")

    minimum_bikes = math.ceil(dock_count * 0.30)
    maximum_bikes = math.floor(dock_count * 0.80)

    target_bikes = math.ceil(dock_count * 0.50)

    add_bikes = 0
    remove_bikes = 0

    if available < minimum_bikes:

        status = "Bike Shortage"
        add_bikes = math.ceil(target_bikes - available)
        recommendation = "Move bicycles to this station"

    elif available > maximum_bikes:

        status = "Dock Shortage"
        remove_bikes = math.ceil(available - target_bikes)
        recommendation = "Redistribute excess bicycles"

    else:

        status = "Balanced"
        recommendation = "No redistribution required"

    return {
        "predicted_available": available,
        "dock_capacity": dock_count,
        "occupancy_percent": round(
            available / dock_count * 100, 2
        ),
        "add_bikes": add_bikes,
        "remove_bikes": remove_bikes,
        "status": status,
        "recommendation": recommendation
    }
if __name__ == "__main__":
  
  print("\n========== BICYCLE ALLOCATION ==========")
  print(allocate_bicycles(668.12, 500))

  print("\n========== TRAFFIC ALLOCATION ==========")
  print(allocate_traffic(5528.50, 6000))

  print("\n========== SUBWAY ALLOCATION ==========")
  print(allocate_subway(264.37, 100, 2))

  print("\n========== BIKE STATION ALLOCATION ==========")
  print(allocate_bike_station(7.97, 20))