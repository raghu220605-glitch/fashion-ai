from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json
import os

app = Flask(__name__)
CORS(app)

# Setup Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Fallback recommendations if the API is down or key is missing
FALLBACK_DATA = {
    "summary": "Currently showing classic recommendations.",
    "outfits": [
        {"name": "The Everyday Classic", "vibe": "Timeless", "top": {"item": "White Linen Shirt"}, "bottom": {"item": "Dark Denim Jeans"}}
    ]
}

SYSTEM_PROMPT = "You are an AI Stylist. Return ONLY JSON. Format: { \"outfits\": [{\"name\": \"\", \"vibe\": \"\", \"top\": {\"item\": \"\"}, \"bottom\": {\"item\": \"\"}}], \"summary\": \"\" }"

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    skin_tone = data.get('skinTone', 'Medium')
    
    try:
        response = model.generate_content(f"{SYSTEM_PROMPT} Suggestions for {skin_tone} skin tone.")
        # Clean potential markdown from AI response
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return jsonify({"success": True, "data": json.loads(clean_json)})
    except Exception as e:
        return jsonify({"success": False, "data": FALLBACK_DATA, "note": "fallback_active"})

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
