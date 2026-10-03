from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Load trained model
MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "cyberbullying_model_v3.pkl"
saved_model = joblib.load(MODEL_PATH)

features = saved_model["features"]
model = saved_model["model"]

print("Model loaded successfully!")


# Home route
@app.route("/")
def home():
    return jsonify({
        "message": "AI Cyberbullying Detection API is running"
    })


# Prediction route
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({
            "error": "Please provide text."
        }), 400

    text = str(data["text"]).strip()

    if not text:
        return jsonify({
            "error": "Text cannot be empty."
        }), 400

    # Convert text into features
    text_features = features.transform([text])

    # Prediction
    prediction = model.predict(text_features)[0]

    # Confidence
    probabilities = model.predict_proba(text_features)[0]
    confidence = max(probabilities) * 100

    return jsonify({
        "text": text,
        "category": prediction,
        "confidence": round(confidence, 2)
    })


if __name__ == "__main__":
    app.run(debug=True)