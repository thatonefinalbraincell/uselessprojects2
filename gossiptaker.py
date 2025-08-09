import google.generativeai as genai
import json

# --- CONFIGURE GEMINI API ---
genai.configure(api_key="AIzaSyB2pY9CDGDe2pMIm6LKaPw3MAU6Js_jStk")

# --- GOSSIP DATABASE ---
gossip_log = []

# --- SASSY BOT PERSONALITY ---
sassy_prompt = """
You are a friendly, gossip-loving best friend, but keep your tone natural and relatable.
- Respond with curiosity, humor, and light teasing, but not too over the top.
- Use emojis sparingly, only when they fit naturally.
- Ask gentle follow-up questions to get more details about the gossip.
- Keep the mood fun and light-hearted, never mean or overly dramatic.
Example:
User: "I saw Alex with someone yesterday."
You: "Oh really? 👀 Was it someone we know, or is this a mystery person?"
"""

# --- FUNCTION TO CHAT & STORE GOSSIP ---
def chat_with_sassy_bot(user_message):
    # Store gossip
    gossip_log.append({"gossip": user_message})

    # Call Gemini API
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
        sassy_prompt + "\nUser: " + user_message
    )

    return response.text

# --- SIMPLE CHAT LOOP ---
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Bye bestie! Here’s all the tea you spilled today:")
        print(json.dumps(gossip_log, indent=2))
        break

    reply = chat_with_sassy_bot(user_input)
    print("SassyBot:", reply)