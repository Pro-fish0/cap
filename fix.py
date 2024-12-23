import requests

# Backend API endpoints
GET_CAPACITY_URL = "http://209.38.41.138/api/shifts/capacity"
SET_CAPACITY_URL = "http://209.38.41.138/api/admin/capacity"

def fetch_shift_capacities(date):
    """
    Fetch capacities for a specific date.

    Args:
        date (str): The date in "YYYY-MM-DD" format.

    Returns:
        list: A list of shift capacities for the given date.
    """
    try:
        response = requests.get(f"{GET_CAPACITY_URL}?date={date}")
        response.raise_for_status()
        data = response.json()
        print(f"📋 Capacities for {date}: {data}")  # Debug the response structure
        return data
    except requests.RequestException as e:
        print(f"❌ Error fetching capacities for {date}: {str(e)}")
        return []

def fix_negative_capacity(date, shift_type, total_capacity, available_capacity):
    """
    Fix negative capacities by resetting them to zero or recalculating.

    Args:
        date (str): The date in "YYYY-MM-DD" format.
        shift_type (str): The shift type (e.g., "M", "E", "N").
        total_capacity (int): The total capacity for the shift.
        available_capacity (int): The available capacity for the shift.

    Returns:
        None
    """
    if available_capacity < 0:
        print(f"⚠️ Negative capacity detected for {date} {shift_type}: {available_capacity}")
        payload = {
            "date": date,
            "shift_type": shift_type,
            "capacity": total_capacity,
        }
        try:
            response = requests.post(SET_CAPACITY_URL, json=payload)
            if response.status_code == 200:
                print(f"✅ Fixed capacity for {date} {shift_type} to {total_capacity}")
            else:
                print(f"❌ Failed to fix capacity for {date} {shift_type}: {response.text}")
        except requests.RequestException as e:
            print(f"❌ Error fixing capacity for {date} {shift_type}: {str(e)}")

def process_month(year, month):
    """
    Process all days in a month and fix negative capacities.

    Args:
        year (int): The year (e.g., 2025).
        month (int): The month (e.g., 1 for January).

    Returns:
        None
    """
    for day in range(1, 32):  # Days in January
        date = f"{year}-{month:02d}-{day:02d}"
        shifts = fetch_shift_capacities(date)
        if not isinstance(shifts, list):
            print(f"❌ Unexpected data format for {date}: {shifts}")
            continue
        for shift in shifts:
            try:
                total_capacity = shift["total"]  # Adjust according to your API response
                available_capacity = shift["available"]  # Adjust according to your API response
                shift_type = shift["shift_type"]  # Adjust according to your API response
                if available_capacity < 0:
                    fix_negative_capacity(date, shift_type, total_capacity, available_capacity)
            except (KeyError, TypeError) as e:
                print(f"❌ Error processing shift for {date}: {str(e)}")

if __name__ == "__main__":
    year = 2025
    month = 1

    print(f"🚀 Processing and fixing capacities for {year}-{month:02d}...")
    process_month(year, month)
    print("🎉 Capacity fixing completed.")
