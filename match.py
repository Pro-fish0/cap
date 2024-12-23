import requests

# Backend API endpoints
SET_CAPACITY_URL = "http://209.38.41.138/api/admin/capacity"

# Desired capacities for January 2025
capacities = {
    "M": [1, 0, 4, 2, 0, 0, 5, 5, 3, 5, 5, 4, 4, 4, 5, 5, 8, 5, 1, 0, 4, 10, 9, 7, 7, 3, 0, 2, 5, 8, 7],
    "E": [8, 11, 10, 12, 6, 6, 4, 4, 11, 10, 10, 6, 0, 0, 2, 9, 9, 9, 9, 6, 4, 3, 7, 12, 12, 11, 10, 7, 5, 4, 8],
    "N": [3, 0, 4, 5, 6, 8, 3, 1, 4, 6, 8, 6, 7, 7, 7, 6, 8, 5, 3, 3, 5, 2, 1, 2, 4, 7, 7, 3, 1, 1, 1],
}

def update_shift_capacity(date, shift_type, capacity):
    """
    Update the capacity for a specific shift on a given date.

    Args:
        date (str): The date in "YYYY-MM-DD" format.
        shift_type (str): The shift type (e.g., "M", "E", "N").
        capacity (int): The capacity to set.

    Returns:
        None
    """
    payload = {
        "date": date,
        "shift_type": shift_type,
        "capacity": capacity,
    }
    try:
        response = requests.post(SET_CAPACITY_URL, json=payload)
        if response.status_code == 200:
            print(f"✅ Updated {shift_type} capacity for {date} to {capacity}")
        else:
            print(f"❌ Failed to update {shift_type} capacity for {date}: {response.text}")
    except requests.RequestException as e:
        print(f"❌ Error updating {shift_type} capacity for {date}: {str(e)}")

def update_capacities(year, month, capacities):
    """
    Update the capacities for all days and shifts in the given month.

    Args:
        year (int): The year (e.g., 2025).
        month (int): The month (e.g., 1 for January).
        capacities (dict): A dictionary containing the capacities for each shift type.

    Returns:
        None
    """
    for day in range(1, 32):  # Days in January
        for shift_type, daily_capacities in capacities.items():
            if day <= len(daily_capacities):
                date = f"{year}-{month:02d}-{day:02d}"
                capacity = daily_capacities[day - 1]
                update_shift_capacity(date, shift_type, capacity)

if __name__ == "__main__":
    year = 2025
    month = 1

    print(f"🚀 Updating capacities for {year}-{month:02d}...")
    update_capacities(year, month, capacities)
    print("🎉 Capacities updated successfully.")
