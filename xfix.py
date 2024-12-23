import requests
import json

API_BASE_URL = "http://209.38.41.138/api"

def set_capacity(date, shift_type, capacity):
    """Set capacity for a specific date and shift type"""
    url = f"{API_BASE_URL}/admin/capacity"
    payload = {
        'date': date,
        'shift_type': shift_type,
        'capacity': capacity
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print(f"Error setting capacity for {date} {shift_type}: {response.text}")
    return response.json()

def fix_capacities():
    # Fixed totals
    TOTALS = {
        'Morning': 12,
        'Evening': 15,
        'Night': 12
    }
    
    # Process each day
    for day in range(1, 32):
        date_str = f"2025-01-{str(day).zfill(2)}"
        
        for shift_type, total in TOTALS.items():
            try:
                print(f"\nSetting {date_str} {shift_type} to total capacity: {total}")
                response = set_capacity(date_str, shift_type, total)
                print(f"Success: {response}")
                
            except Exception as e:
                print(f"Error setting capacity for {date_str} {shift_type}: {str(e)}")

if __name__ == "__main__":
    try:
        fix_capacities()
        print("\nCapacity update completed!")
    except Exception as e:
        print(f"Script failed: {str(e)}")
