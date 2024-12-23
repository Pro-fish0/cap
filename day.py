import requests

# Backend API URL
API_URL = "http://209.38.41.138/api/shifts/capacity"  # Update with your backend URL

def fetch_capacities(api_url, date):
    """
    Fetch shift capacities for a given month.

    Args:
        api_url (str): The backend API endpoint.
        date (str): The date in "YYYY-MM-DD" format (1st day of the desired month).

    Returns:
        dict: Shift capacities grouped by day and shift type.
    """
    try:
        response = requests.get(api_url, params={"date": date})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error fetching capacities: {str(e)}")
        return None


if __name__ == "__main__":
    year = 2025
    month = 1
    date = f"{year}-{month:02d}-01"  # Use the 1st day of the month to fetch data

    print("🚀 Fetching capacities...")
    capacities = fetch_capacities(API_URL, date)

    if capacities:
        print(f"🎉 Capacities for {year}-{month:02d}:")
        print("{:<5} {:<10} {:<10} {:<10}".format("Day", "Shift", "Total", "Available"))
        print("-" * 40)
        for key, value in capacities.items():
            day, shift = key.split("_")
            print("{:<5} {:<10} {:<10} {:<10}".format(day, shift, value['total'], value['available']))
    else:
        print("❌ Failed to fetch capacities.")
