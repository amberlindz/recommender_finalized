from django.db import models

class ChatMessage(models.Model):
    """Model to store chat history."""
    session_id = models.CharField(max_length=100)
    sender = models.CharField(max_length=10)  # 'user' or 'bot'
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender}: {self.message[:50]}"
