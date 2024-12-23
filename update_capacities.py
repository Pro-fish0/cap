import requests

# Backend API URL (change this to match your backend endpoint)
API_URL = "http://209.38.41.138/api/admin/capacity"

# Data for capacities (adjust as needed)
capacity_data = {
    "M": [1, 0, 4, 2, 0, 0, 5, 5, 3, 5, 5, 4, 4, 4, 5, 5, 8, 5, 1, 0, 4, 10, 9, 7, 7, 3, 0, 2, 5, 8, 7],
    "E": [8, 11, 10, 12, 6, 6, 4, 4, 11, 10, 10, 6, 0, 0, 2, 9, 9, 9, 9, 6, 4, 3, 7, 12, 12, 11, 10, 7, 5, 4, 8],
    "N": [3, 0, 4, 5, 6, 8, 3, 1, 4, 6, 8, 6, 7, 7, 7, 6, 8, 5, 3, 3, 5, 2, 1, 2, 4, 7, 7, 3, 1, 1, 1]
}

# Year and month for the update
YEAR = 2025
MONTH = 1


def update_capacity(api_url, data):
    """
    Update shift capacities via API calls.

    Args:
        api_url (str): The backend API endpoint.
        data (dict): Capacity data structured by shift type and day.

    """
    for shift_type, capacities in data.items():
        for day, capacity in enumerate(capacities, start=1):
            date = f"{YEAR}-{MONTH:02d}-{day:02d}"
            payload = {
                "date": date,
                "shift_type": shift_type,
                "capacity": capacity
            }
            try:
                response = requests.post(api_url, json=payload)
                if response.status_code == 200:
                    print(f"✅ Updated {shift_type} capacity for {date} to {capacity}")
                else:
                    print(f"❌ Failed to update {shift_type} capacity for {date}: {response.text}")
            except requests.RequestException as e:
                print(f"❌ Error updating {shift_type} capacity for {date}: {str(e)}")


if __name__ == "__main__":
    print("🚀 Starting capacity update...")
    update_capacity(API_URL, capacity_data)
    print("🎉 Capacity update completed!")
