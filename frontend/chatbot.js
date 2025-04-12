document.addEventListener('DOMContentLoaded', function() {
    const chatbot = document.getElementById('chatbot-taskbar');
    
    // Show after slight delay
    setTimeout(() => {
        chatbot.style.bottom = '20px';
    }, 1500);

    // Scroll-triggered chatbot taskbar
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            chatbot.style.bottom = '20px';
        } else {
            chatbot.style.bottom = '-100px';
        }
    });

    window.sendMessage = async function() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();
        
        if (message) {
            try {
                const response = await fetch('/api/chatbot', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                alert(data.response);
                input.value = "";
            } catch (error) {
                alert("Error sending message. Please try again.");
            }
        } else {
            alert("Please enter your question or concern.");
        }
    }
});