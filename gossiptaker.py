from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# --- CONFIGURE GEMINI API ---
genai.configure(api_key="AIzaSyB2pY9CDGDe2pMIm6LKaPw3MAU6Js_jStk")

# This list will store a log of the gossip.
gossip_log = []

# This is the system prompt for the "Give Gossip" bot.
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
    """
    Sends a user message to the Gemini API with the sassy persona prompt
    and returns the AI's reply.
    """
    # Append the user's new gossip to our log.
    gossip_log.append({"gossip": user_message})

    # Create the full prompt by combining the persona and the user message.
    full_prompt = sassy_prompt + "\nUser: " + user_message

    # Generate content using the Gemini API.
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
        full_prompt
    )
    return response.text

@app.route('/')
def index():
    """
    This route serves your main HTML file.
    The 'render_template' function looks for files in the 'templates' folder.
    """
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    This route handles the chat messages from your "Give Gossip" modal.
    It receives the message, processes it, and sends back a reply.
    """
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "You gotta say something first!"})

    # The frontend JavaScript handles the "bye" message, so this block is not strictly necessary,
    # but it's good to have for robustness.
    if user_message.lower() in ["exit", "quit", "bye"]:
        goodbye_msg = "👋 Byeee! Seriously, that was so much fun!"
        return jsonify({"reply": goodbye_msg})

    # Get the sassy bot's reply.
    reply = chat_with_sassy_bot(user_message)
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)