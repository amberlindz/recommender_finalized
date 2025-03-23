import json
import requests
from django.conf import settings
from ..utils import get_all_restaurants

class ClaudeAPI:
    """Integration with Claude 3.7 for natural language processing."""
    
    API_URL = "https://api.anthropic.com/v1/messages"
    
    def __init__(self):
        self.api_key = settings.CLAUDE_API_KEY
        self.model = "claude-3-7-sonnet-20250219"
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
    
    def get_response(self, prompt, session_id):
        """Get a response from Claude based on user input."""
        # Get restaurant data
        restaurant_data = get_all_restaurants()
        
        # Include restaurant data in system prompt
        system_prompt = self._get_system_prompt(restaurant_data)
        
        # Get chat history for context
        chat_history = self._get_chat_history(session_id)
        
        # Prepare request body
        data = {
            "model": self.model,
            "system": system_prompt,
            "messages": chat_history + [{"role": "user", "content": prompt}],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.API_URL, headers=self.headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            
            # Extract actual response content
            message_content = response_data.get('content', [])
            full_text = ""
            for content in message_content:
                if content.get('type') == 'text':
                    full_text += content.get('text', '')
            
            # Check if the response includes restaurant recommendations
            recommendations = self._extract_restaurant_recommendations(full_text)
            
            return full_text, recommendations
            
        except Exception as e:
            print(f"Error calling Claude API: {str(e)}")
            return "I'm having trouble connecting right now. Please try again later.", []
    
    def _get_system_prompt(self, restaurant_data):
        """Create system prompt with restaurant context."""
        base_prompt = (
            "You are a helpful restaurant recommendation chatbot for Los Angeles. "
            "Your name is Mady. Be friendly, helpful, and concise in your responses. "
            "Always maintain a conversational and positive tone. "
            "Only recommend restaurants from the provided dataset. "
            "Do not use foul or inappropriate language. "
            "If the user asks for a specific cuisine or location not in your database, "
            "politely explain that you only have information about certain restaurants "
            "and offer alternatives from what you do know about."
        )
        
        base_prompt += f"\n\nHere's the restaurant data you can use for recommendations:\n{json.dumps(restaurant_data)}"
        
        return base_prompt
    
    def _get_chat_history(self, session_id, max_messages=5):
        """Retrieve recent chat history for context."""
        from ..models import ChatMessage
        
        messages = ChatMessage.objects.filter(session_id=session_id).order_by('-timestamp')[:max_messages]
        messages = reversed(list(messages))  # Reverse to get chronological order
        
        formatted_history = []
        for msg in messages:
            role = "user" if msg.sender == "user" else "assistant"
            formatted_history.append({"role": role, "content": msg.message})
        
        return formatted_history
    
    def _extract_restaurant_recommendations(self, response_text):
        """Extract restaurant IDs from Claude's response."""
        # Get restaurant data
        restaurants = get_all_restaurants()
        
        recommended_restaurants = []
        for restaurant in restaurants:
            if restaurant['name'].lower() in response_text.lower():
                recommended_restaurants.append(restaurant)
        
        return recommended_restaurants[:5]  # Limit to 5 recommendations

def get_claude_response(user_message, session_id):
    """Get response from Claude API with restaurant data context."""
    # Initialize Claude API and get response
    claude = ClaudeAPI()
    response, recommendations = claude.get_response(user_message, session_id)
    
    # Save the user message and bot response to the database
    from ..models import ChatMessage
    ChatMessage.objects.create(session_id=session_id, sender="user", message=user_message)
    ChatMessage.objects.create(session_id=session_id, sender="bot", message=response)
    
    return response, recommendations