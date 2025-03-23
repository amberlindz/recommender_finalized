from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid
from .utils.claude_integration import get_claude_response
from .utils.geolocation import geocode_address
from .utils import get_all_restaurants

def index(request):
    """Render the main chatbot interface."""
    return render(request, 'chatbot/index.html')

@csrf_exempt
def chat_api(request):
    """API endpoint for chatbot interactions."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            session_id = data.get('session_id', str(uuid.uuid4()))
            
            # Get response from Claude
            response, recommendations = get_claude_response(message, session_id)
            
            return JsonResponse({
                'response': response,
                'recommendations': recommendations
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST requests are supported'}, status=405)

def restaurants_api(request):
    """API endpoint to get all restaurants."""
    restaurants = get_all_restaurants()
    return JsonResponse(restaurants, safe=False)

def geocode_api(request):
    """API endpoint for geocoding addresses."""
    address = request.GET.get('address', '')
    if address:
        lat, lng = geocode_address(address)
        if lat and lng:
            return JsonResponse({'lat': lat, 'lng': lng})
    
    return JsonResponse({'error': 'Unable to geocode address'}, status=400)