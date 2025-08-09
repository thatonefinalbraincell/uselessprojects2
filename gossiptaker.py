from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# --- CONFIGURE GEMINI API ---
genai.configure(api_key="AIzaSyB2pY9CDGDe2pMIm6LKaPw3MAU6Js_jStk")

gossip_log = []

sassy_prompt = """
You are a sassy, gossip-loving best friend.
- Always respond with dramatic reactions, slang, and playful teasing.
- Use emojis and exaggerated tone.
- Always try to get MORE details about the gossip.
- Keep it light-hearted, never mean.
Example:
User: "I saw Alex with someone yesterday."
You: "OMG 😱 STOP IT. Was it who I think it was?? Details, NOW 👀"
"""

def chat_with_sassy_bot(user_message):
    gossip_log.append({"gossip": user_message})

    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
        sassy_prompt + "\nUser: " + user_message
    )
    return response.text

# Frontend HTML (using Flask’s render_template_string for simplicity)
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>SassyBot Tea Time</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 30px; }
    #chatbox { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: auto; }
    .message { margin: 10px 0; }
    .user { color: blue; }
    .bot { color: green; }
    button { margin: 5px; padding: 10px 20px; }
    #inputSection { margin-top: 20px; }
  </style>
</head>
<body>

<h1>Welcome to SassyBot Tea Time ☕️</h1>

<div id="choiceSection">
  <p>Do you want to <b>Get the tea</b> or <b>Know the tea</b>?</p>
  <button onclick="startChat('get')">Get the tea</button>
  <button onclick="startChat('know')">Know the tea</button>
</div>

<div id="chatSection" style="display:none;">
  <div id="chatbox"></div>

  <div id="inputSection">
    <input type="text" id="userInput" placeholder="Spill the tea..." style="width: 300px;" />
    <button onclick="sendMessage()">Send</button>
  </div>
</div>

<script>
  let chatting = false;

  function startChat(choice) {
    chatting = true;
    document.getElementById('choiceSection').style.display = 'none';
    document.getElementById('chatSection').style.display = 'block';

    addMessage("bot", `Alright, you chose to "${choice} the tea". Spill away!`);
  }

  function addMessage(sender, text) {
    const chatbox = document.getElementById('chatbox');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message ' + sender;
    msgDiv.textContent = (sender === 'user' ? 'You: ' : 'SassyBot: ') + text;
    chatbox.appendChild(msgDiv);
    chatbox.scrollTop = chatbox.scrollHeight;
  }

  async function sendMessage() {
    const input = document.getElementById('userInput');
    const msg = input.value.trim();
    if (!msg) return;

    addMessage('user', msg);
    input.value = '';

    if (msg.toLowerCase() === 'bye' || msg.toLowerCase() === 'exit' || msg.toLowerCase() === 'quit') {
      addMessage('bot', '👋 Byeee! Seriously, that was so much fun!');
      chatting = false;
      return;
    }

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: msg})
      });
      const data = await response.json();
      addMessage('bot', data.reply);
    } catch (error) {
      addMessage('bot', 'Oops, something went wrong. Try again!');
    }
  }
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(index_html)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "You gotta say something first!"})

    if user_message.lower() in ["exit", "quit", "bye"]:
        goodbye_msg = "👋 Byeee! Seriously, that was so much fun!"
        return jsonify({"reply": goodbye_msg})

    reply = chat_with_sassy_bot(user_message)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
