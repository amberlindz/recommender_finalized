from django.apps import AppConfig
import os
from django.conf import settings

class ChatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbot'
    
    def ready(self):
        # Create necessary directories if they don't exist
        os.makedirs(os.path.dirname(settings.RESTAURANT_JSON_PATH), exist_ok=True)
