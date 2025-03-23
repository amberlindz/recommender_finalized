from ..utils import get_all_restaurants

def filter_restaurants(neighborhood=None):
    """Filter restaurants based on neighborhood."""
    restaurants = get_all_restaurants()
    
    if neighborhood:
        restaurants = [r for r in restaurants if r['neighborhood'].lower() == neighborhood.lower()]
    
    return restaurants

def get_restaurant_recommendations(location=None, limit=5):
    """Get restaurant recommendations based on location."""
    restaurants = get_all_restaurants()
    
    # Filter by neighborhood if location specified
    if location:
        restaurants = [r for r in restaurants if location.lower() in r['neighborhood'].lower()]
    
    # Limit the number of recommendations
    restaurants = restaurants[:limit]
    
    return restaurants