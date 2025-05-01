from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

app = Flask(__name__)

GOOGLE_API_KEY = 'AIzaSyAtu2Q9iE17N0xuuecIs3Y26WPjYBh04Ho'
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Smart Packing Assistant</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #001F54; /* navy blue */
            --secondary-color: #56CCF2;
            --background-color: #F2F8FC;
            --text-color: #333;
        }

        body {
            font-family: 'Poppins', sans-serif;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            background: linear-gradient(rgba(242, 248, 252, 0.7), rgba(242, 248, 252, 0.7)),
            url('https://mitsubishisolutions.com/wp-content/uploads/2023/10/bigstock-Arm-Robot-Ai-Manufacture-Box-P-471835205.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }

        header .left-logo img {
            height: 60px;
            border-radius: 10px;
        }

        .center-title {
            text-align: center;
            flex-grow: 1;
        }

        header h1 {
            color: var(--primary-color);
            font-size: 1.8em;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
            justify-content: center;
        }

        header p {
            color: #666;
            margin-top: 5px;
            font-size: 1em;
        }

        .profile-info {
            text-align: right;
            font-size: 0.9em;
            color: #555;
            white-space: nowrap;
        }

        .chat-container {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .chat-header {
            background: var(--primary-color); /* navy blue */
            color: white;
            padding: 15px 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .status-indicator {
            width: 8px;
            height: 8px;
            background: #4CAF50;
            border-radius: 50%;
            margin-left: auto;
        }

        #chat-messages {
            height: 400px;
            overflow-y: auto;
            padding: 20px;
        }

        .message {
            margin-bottom: 15px;
            padding: 12px 15px;
            border-radius: 10px;
            max-width: 80%;
        }

        .bot-message {
            background: var(--primary-color); /* navy blue */
            color: white;
            align-self: flex-start;
            margin-right: auto;
        }

        .user-message {
            background: var(--secondary-color);
            color: white;
            align-self: flex-end;
            margin-left: auto;
        }

        .chat-input {
            display: flex;
            padding: 15px;
            gap: 10px;
            background: #f5f5f5;
            border-top: 1px solid #eee;
        }

        #user-input {
            flex-grow: 1;
            padding: 10px 15px;
            border: 1px solid #ddd;
            border-radius: 25px;
            outline: none;
        }

        .chat-input button {
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .chat-input button:hover {
            background: var(--secondary-color);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="left-logo">
                <img src="https://i.pinimg.com/originals/c9/12/d4/c912d49f5f63e3c25aae2465f7577e7a.png" alt="LPU Logo">
            </div>

            <div class="center-title">
                <h1><i class="fas fa-suitcase-rolling"></i> AI Smart Packing Assistant</h1>
                <p>Plan smarter. Pack better. Travel lighter.</p>
            </div>

            <div class="profile-info">
                <div><strong>Rahul</strong> (12309827)</div>
                <div><strong>Ramit Phul</strong> (12309069)</div>
                <div><strong>Ayan Khan</strong> (12313863)</div>
            </div>
        </header>

        <div class="chat-container">
            <div class="chat-header">
                <i class="fas fa-robot"></i>
                <span>Packing Assistant</span>
                <div class="status-indicator"></div>
            </div>

            <div id="chat-messages">
                <div class="message bot-message">
                    Hello! I'm your AI Smart Packing Assistant. Tell me your destination, weather, activities, or trip duration — I'll suggest exactly what you should pack. Where are you headed?
                </div>
            </div>

            <div class="chat-input">
                <input type="text" id="user-input" placeholder="Where are you traveling to? What do you need help packing for?">
                <button onclick="sendMessage()"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;

            addMessage(message, 'user-message');
            input.value = '';

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                addMessage(data.reply, 'bot-message');
            } catch (error) {
                addMessage('Sorry, I encountered an error. Please try again.', 'bot-message');
            }
        }

        function addMessage(message, className) {
            const chatMessages = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + className;
            messageDiv.textContent = message;
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        document.getElementById('user-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    try:
        response = model.generate_content(message)
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)