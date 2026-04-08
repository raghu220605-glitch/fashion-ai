from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json
import os

app = Flask(__name__)
CORS(app)

# Configure Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# The Fallback Option: If the API fails, return this instead
DEFAULT_FALLBACK = {
    "color_analysis": {
        "best_colors": [{"color": "Navy Blue", "hex": "#000080", "reason": "Universal classic"}],
        "colors_to_avoid": [],
        "palette_summary": "We're having trouble reaching the AI Stylist, but here are some timeless classics."
    },
    "outfits": [
        {
            "id": 1,
            "name": "The Timeless Casual",
            "vibe": "Classic",
            "top": {"item": "White button-down shirt"},
            "bottom": {"item": "Dark indigo jeans"},
            "shoes": {"item": "Clean white sneakers"}
        }
    ],
    "summary": "Currently showing offline recommendations."
}

SYSTEM_PROMPT = "You are a professional fashion stylist. Return ONLY a JSON object. Format: { \"outfits\": [{\"name\": \"\", \"vibe\": \"\", \"top\": {\"item\": \"\"}, \"bottom\": {\"item\": \"\"}}], \"summary\": \"\" }"

@app.route("/api/analyze", methods=["POST"])
def analyze_fashion():
    data = request.get_json()
    skin_tone = data.get('skinTone', 'Medium')
    item_type = data.get('itemType', 'outfit')

    user_prompt = f"Provide 3 {item_type} suggestions for someone with {skin_tone} skin tone."

    try:
        # Call Gemini API
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nUser Request: {user_prompt}")
        
        # Parse JSON from response
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean_text)
        
        return jsonify({"success": True, "data": result})

    except Exception as e:
        print(f"API Error: {e}")
        # FALLBACK: Return the default hardcoded data if API fails
        return jsonify({"success": False, "data": DEFAULT_FALLBACK, "note": "fallback_active"})

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
