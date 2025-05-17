document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const messageContainer = document.getElementById('messageContainer');
    const newChatBtn = document.getElementById('newChatBtn');

    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;
        
        addMessage('user', message);
        userInput.value = '';
        
        const typingId = showTypingIndicator();
        
        try {
            const formData = new FormData();
            formData.append('message', message);
            
            const response = await fetch('/api/v1/chat', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            removeTypingIndicator(typingId);
            addMessage('assistant', data.response);
            
        } catch (error) {
            console.error('Error:', error);
            removeTypingIndicator(typingId);
            addMessage('assistant', 'Error: Could not get response');
        }
    });

    // New chat functionality
    newChatBtn.addEventListener('click', async function() {
        try {
            const response = await fetch('/api/v1/new_chat', {
                method: 'POST'
            });
            
            const data = await response.json();
            if (data.status === 'success') {
                messageContainer.innerHTML = `
                    <div class="welcome-message">
                        <h2>New Chat Started</h2>
                        <p>Ask me anything about internet history, GDPR, or digital culture</p>
                        <div class="suggestions">
                            <div class="suggestion">Explain the history of the internet</div>
                            <div class="suggestion">What are the key GDPR requirements?</div>
                            <div class="suggestion">How has digital culture evolved?</div>
                        </div>
                    </div>
                `;
                setupSuggestions();
            }
        } catch (error) {
            console.error('Error starting new chat:', error);
        }
    });

    // Helper functions
    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;
        messageDiv.innerHTML = role === 'assistant' ? marked.parse(content) : content;
        messageContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message ai-message typing-indicator';
        typingDiv.id = 'typing-' + Date.now();
        typingDiv.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
        messageContainer.appendChild(typingDiv);
        scrollToBottom();
        return typingDiv.id;
    }

    function setupSuggestions() {
        document.querySelectorAll('.suggestion').forEach(item => {
            item.addEventListener('click', function() {
                userInput.value = this.textContent;
                userInput.focus();
            });
        });
    }

    // Initialize
    setupSuggestions();
});