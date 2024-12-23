import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://209.38.41.138/api"  # Update this to match your API URL

# Standard capacities for January 2025
STANDARD_CAPACITIES = {
    'Morning': 12,
    'Evening': 15,
    'Night': 12
}

def get_current_capacities():
    """Get current capacity data for January 2025"""
    response = requests.get(f"{API_BASE_URL}/shifts/capacity", params={
        'date': '2025-01-01'
    })
    if response.status_code != 200:
        raise Exception(f"Failed to get capacities: {response.text}")
    return response.json()

def set_capacity(date, shift_type, capacity):
    """Set capacity for a specific date and shift type"""
    response = requests.post(f"{API_BASE_URL}/admin/capacity", json={
        'date': date,
        'shift_type': shift_type,
        'capacity': capacity
    })
    if response.status_code != 200:
        raise Exception(f"Failed to set capacity: {response.text}")
    return response.json()

def fix_january_capacities():
    print("Getting current capacity data...")
    current_data = get_current_capacities()
    
    print("\nAnalyzing and fixing capacities for January 2025...")
    for day in range(1, 32):
        date_str = f"2025-01-{str(day).zfill(2)}"
        
        for shift_type, standard_capacity in STANDARD_CAPACITIES.items():
            key = f"{day}_{shift_type}"
            current = current_data.get(key, {})
            taken = current.get('taken', 0)
            
            # Set the total capacity to standard value
            print(f"\nProcessing {date_str} {shift_type}:")
            print(f"Current - Total: {current.get('total', 0)}, Taken: {taken}, Available: {current.get('available', 0)}")
            
            try:
                result = set_capacity(date_str, shift_type, standard_capacity)
                print(f"Updated - Total: {standard_capacity}, Taken: {taken}, Free: {standard_capacity - taken}")
            except Exception as e:
                print(f"Error updating {date_str} {shift_type}: {str(e)}")

if __name__ == "__main__":
    try:
        fix_january_capacities()
        print("\nCapacity update completed!")
    except Exception as e:
        print(f"Script failed: {str(e)}")
