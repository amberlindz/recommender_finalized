import json
import os
from django.conf import settings

def get_restaurant_data():
    """Load restaurant data from JSON file."""
    try:
        with open(settings.RESTAURANT_JSON_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading restaurant data: {str(e)}")
        return {"metadata": {}, "restaurants": []}
        
def get_all_restaurants():
    """Get all restaurants from JSON file."""
    data = get_restaurant_data()
    return data.get("restaurants", [])
    
def get_all_neighborhoods():
    """Get all unique neighborhoods from JSON file."""
    data = get_restaurant_data()
    return data.get("metadata", {}).get("neighborhoods", [])