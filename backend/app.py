from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Professional Style Matrix (Logic instead of API Key)
STYLE_DB = {
    "fair": {
        "summary": "Cool jewel tones and pastels provide a stunning contrast for fair skin.",
        "outfits": [
            {"name": "Emerald Elegance", "color": "#50C878", "top": "Emerald Silk Blouse", "bottom": "Black Tailored Trousers", "img": "emerald-fashion"},
            {"name": "Royal Casual", "color": "#4169E1", "top": "Royal Blue Knit", "bottom": "White Linen Pants", "img": "blue-outfit"},
            {"name": "Soft Pastel", "color": "#FFD1DC", "top": "Blush Pink Blazer", "bottom": "Light Grey Chinos", "img": "pastel-fashion"}
        ]
    },
    "medium": {
        "summary": "Earth tones and warm shades highlight the natural golden glow of medium skin.",
        "outfits": [
            {"name": "Terracotta Chic", "color": "#E2725B", "top": "Terracotta Wrap Top", "bottom": "Beige Wide-Leg Pants", "img": "terracotta-clothing"},
            {"name": "Olive Utility", "color": "#808000", "top": "Olive Cargo Shirt", "bottom": "Dark Wash Denim", "img": "olive-fashion"},
            {"name": "Golden Hour", "color": "#FFDB58", "top": "Mustard Yellow Sweater", "bottom": "Cream Skirt", "img": "yellow-outfit"}
        ]
    },
    "dark": {
        "summary": "High-saturation colors and vibrant hues pop brilliantly against deep skin tones.",
        "outfits": [
            {"name": "Cobalt Power", "color": "#0047AB", "top": "Cobalt Blue Suit", "bottom": "Matching Trousers", "img": "cobalt-fashion"},
            {"name": "Citrus Burst", "color": "#FFEF00", "top": "Bright Yellow Maxi", "bottom": "Gold Accessories", "img": "vibrant-fashion"},
            {"name": "Ruby Radiance", "color": "#E0115F", "top": "Ruby Red Silk Shirt", "bottom": "White High-Waist Jeans", "img": "red-outfit"}
        ]
    }
}

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    tone = data.get('skinTone', 'medium').lower()
    item = data.get('itemType', 'outfit').lower()
    
    # Fetch data from matrix
    style_data = STYLE_DB.get(tone, STYLE_DB['medium'])
    
    # Filter or customize based on itemType
    final_outfits = []
    for o in style_data['outfits']:
        modified = o.copy()
        if item != "outfit":
            modified['name'] = f"Suggested {item.capitalize()}"
        final_outfits.append(modified)

    return jsonify({"success": True, "data": {"outfits": final_outfits, "summary": style_data['summary']}})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
