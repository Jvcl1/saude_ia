document.addEventListener('DOMContentLoaded', function() {
    // Chat functionality
    const sendButton = document.getElementById('sendButton');
    const userInput = document.getElementById('userInput');
    
    if (sendButton && userInput) {
        sendButton.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    function sendMessage() {
        const userInput = document.getElementById('userInput');
        const message = userInput.value.trim();
        
        if (message) {
            const chatContainer = document.getElementById('chatContainer');
            const userMessageDiv = document.createElement('div');
            userMessageDiv.className = 'user-message';
            userMessageDiv.textContent = message;
            chatContainer.appendChild(userMessageDiv);
            
            userInput.value = '';
            chatContainer.scrollTop = chatContainer.scrollHeight;
            
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                const botMessageDiv = document.createElement('div');
                botMessageDiv.className = 'bot-message';
                botMessageDiv.textContent = data.response;
                chatContainer.appendChild(botMessageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            });
        }
    }
});