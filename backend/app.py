from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS library
import google.generativeai as genai
import json
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# --- CONFIGURE GEMINI API ---
# IMPORTANT: You MUST replace "YOUR_GEMINI_API_KEY" with your actual Gemini API key.
# This is the single most important step.
genai.configure(api_key="AIzaSyB2pY9CDGDe2pMIm6LKaPw3MAU6Js_jStk")

# --- SASSY BOT PERSONALITY (FOR 'SPILL THE TEA' SECTION) ---
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

# --- RELATABLE BOT PERSONALITY (FOR 'GET THE SCOOP' SECTION) ---
relatable_prompt = """
You are a friendly, relatable gossip enthusiast who loves a good story.
- Respond with curiosity, humor, and light teasing, but keep your tone natural.
- Use emojis sparingly, only when they fit naturally.
- Ask gentle follow-up questions to get more details about the gossip.
- Keep the mood fun and light-hearted, never mean or overly dramatic.
Example:
User: "I saw Alex with someone yesterday."
You: "Oh really? 👀 Was it someone we know, or is this a mystery person?"
"""

# --- ROUTE FOR SPILL THE TEA ---
@app.route("/spill_tea", methods=["POST"])
def spill_tea():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Exponential backoff for API calls
    retries = 0
    while retries < 5:
        try:
            response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
                sassy_prompt + "\nUser: " + user_message
            )
            return jsonify({"reply": response.text})
        except Exception as e:
            print(f"API call failed, retrying in {2**retries} seconds... Error: {e}")
            time.sleep(2**retries)
            retries += 1
    
    return jsonify({"error": "Failed to get response from Gemini API after multiple retries"}), 500


# --- ROUTE FOR GET THE SCOOP ---
@app.route("/get_scoop", methods=["POST"])
def get_scoop():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Exponential backoff for API calls
    retries = 0
    while retries < 5:
        try:
            response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
                relatable_prompt + "\nUser: " + user_message
            )
            return jsonify({"reply": response.text})
        except Exception as e:
            print(f"API call failed, retrying in {2**retries} seconds... Error: {e}")
            time.sleep(2**retries)
            retries += 1
            
    return jsonify({"error": "Failed to get response from Gemini API after multiple retries"}), 500

if __name__ == "__main__":
    app.run(debug=True)
    