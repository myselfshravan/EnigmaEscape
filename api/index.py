from flask import Flask, request, jsonify
from game import GameValidator, levels
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
validator = GameValidator()

@app.route("/api/validate", methods=["POST"])
def validate_response():
    try:
        data = request.get_json()
        
        if not data or "level" not in data or "prompt" not in data:
            return jsonify({
                "error": "Missing required fields: level and prompt"
            }), 400

        level_num = data["level"]
        prompt = data["prompt"]

        # Validate level number
        if not (0 <= level_num < len(levels)):
            return jsonify({
                "error": f"Invalid level number. Must be between 0 and {len(levels) - 1}"
            }), 400

        # Get validation result
        result = validator.validate_response(levels[level_num], prompt)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

@app.route("/api/levels", methods=["GET"])
def get_levels():
    return jsonify([{
        "name": level.name,
        "model": level.model,
        "max_token": level.max_token,
        "points": level.points,
        "description": level.description,
        "clue": level.clue,
        "phrase": level.phrase
    } for level in levels])

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "environment": os.getenv("VERCEL_ENV", "development")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)), debug=True)
