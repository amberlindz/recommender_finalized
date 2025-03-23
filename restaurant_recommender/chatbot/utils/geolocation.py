import requests
import math
from ..utils import get_all_restaurants

def geocode_address(address):
    """Convert an address to latitude and longitude using Nominatim service."""
    try:
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }
        
        # Add a user agent as required by the Nominatim usage policy
        headers = {
            "User-Agent": "RestaurantRecommenderApp/1.0"
        }
        
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        if data and len(data) > 0:
            return float(data[0]["lat"]), float(data[0]["lon"])
        
        return None, None
    
    except Exception as e:
        print(f"Error geocoding address: {str(e)}")
        return None, None

def get_restaurants_in_radius(lat, lng, radius_km=5):
    """Find restaurants within a certain radius of a point."""
    restaurants = get_all_restaurants()
    
    # Filter restaurants that have geocoded coordinates
    # (For this simplified version, we'll assume all restaurants have coordinates)
    result = []
    for restaurant in restaurants:
        # In a real implementation, you would have latitude/longitude values in your JSON
        # For now, we'll geocode addresses on-the-fly when needed
        address = restaurant['address']
        restaurant_lat, restaurant_lng = geocode_address(address)
        
        if restaurant_lat and restaurant_lng:
            # Calculate distance using Haversine formula
            R = 6371.0  # Earth radius in km
            dlat = math.radians(restaurant_lat - lat)
            dlng = math.radians(restaurant_lng - lng)
            a = (math.sin(dlat/2)**2 + 
                 math.cos(math.radians(lat)) * math.cos(math.radians(restaurant_lat)) * 
                 math.sin(dlng/2)**2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = R * c
            
            if distance <= radius_km:
                result.append({
                    'restaurant': restaurant,
                    'distance': distance
                })
    
    # Sort by distance
    result.sort(key=lambda x: x['distance'])
    
    return result