// static/script.js
$(document).ready(function() {
    // ... (previous JavaScript code)

    // New function to send user input to the server
    function sendUserInputToServer(userInput) {
        $.ajax({
            type: 'POST',
            url: '/predict_emotion',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({ text: userInput }),
            success: function(response) {
                var emotion = response.emotion;
                displayMessage("Bot: I detected you're feeling " + emotion + ".", 'bot');
            },
            error: function(error) {
                console.error('Error predicting emotion:', error);
                displayMessage('Bot: Error predicting emotion.', 'bot');
            }
        });
    }

    var chatbotButton = document.getElementById("chatbot-send-btn");
    chatbotButton.onclick = handleUserInput;
    var chatbotInput = document.getElementById("chatbot-input");

    // Override handleUserInput function to send input to server
    function handleUserInput() {
        var userInput = chatbotInput.value.trim();
        console.log(userInput)
        if (userInput !== '') {
            displayMessage("You: " + userInput, 'user');
            sendUserInputToServer(userInput);
            chatbotInput.value('');
        }
    }
    

    

    // ... (remaining JavaScript code)
});
