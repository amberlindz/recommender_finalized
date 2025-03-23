// Get DOM elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// Generate a unique session ID
let sessionId = localStorage.getItem('chatSessionId');
if (!sessionId) {
    sessionId = 'session_' + Date.now();
    localStorage.setItem('chatSessionId', sessionId);
}

// Add event listener for send button
sendButton.addEventListener('click', sendMessage);

// Add event listener for Enter key
userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Function to send message
function sendMessage() {
    const message = userInput.value.trim();
    
    if (message) {
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input
        userInput.value = '';
        
        // Show typing indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'message bot-message typing-indicator';
        typingIndicator.innerHTML = 'Thinking<span>.</span><span>.</span><span>.</span>';
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Send to backend
        fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            }),
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            chatMessages.removeChild(typingIndicator);
            
            // Add bot response to chat
            addMessage(data.response, 'bot');
            
            // Highlight recommended restaurants on the map
            if (data.recommendations && data.recommendations.length > 0) {
                const recommendationIds = data.recommendations.map(r => r.id);
                highlightRestaurants(recommendationIds);
            }
        })
        .catch(error => {
            // Remove typing indicator
            chatMessages.removeChild(typingIndicator);
            
            // Add error message
            addMessage('Sorry, there was an error processing your request. Please try again.', 'bot');
            console.error('Error:', error);
        });
    }
}

// Function to add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.textContent = text;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}