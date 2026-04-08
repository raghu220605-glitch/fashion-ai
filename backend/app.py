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

# Fallback data if the API fails
DEFAULT_FALLBACK = {
    "outfits": [
        {
            "name": "Classic Essential",
            "vibe": "Timeless",
            "top": {"item": "White button-down shirt"},
            "bottom": {"item": "Dark denim jeans"},
            "price": "₹1,999"
        }
    ],
    "summary": "Showing offline classic recommendations."
}

SYSTEM_PROMPT = """You are a fashion stylist. Return ONLY a JSON object. 
Format: { "outfits": [{"name": "", "vibe": "", "top": {"item": ""}, "bottom": {"item": ""}, "price": ""}], "summary": "" }"""

@app.route("/api/analyze", methods=["POST"])
def analyze_fashion():
    data = request.get_json()
    style = data.get('style', 'Casual')
    description = data.get('description', '')

    user_prompt = f"Provide 3 {style} outfit suggestions. Context: {description}"

    try:
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nUser: {user_prompt}")
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean_text)
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "data": DEFAULT_FALLBACK, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
