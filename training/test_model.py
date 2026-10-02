import joblib

# Load trained model
saved_model = joblib.load("model/cyberbullying_model_v3.pkl")

features = saved_model["features"]
model = saved_model["model"]

print("Model loaded successfully!")


def predict_message(text):

    # Convert text into TF-IDF features
    text_features = features.transform([text])

    # Predict category
    prediction = model.predict(text_features)[0]

    # Get confidence
    probabilities = model.predict_proba(text_features)[0]
    confidence = max(probabilities) * 100

    return prediction, confidence


# --------------------------------------------------
# NEW UNSEEN TEST MESSAGES
# --------------------------------------------------

test_messages = [
    # Non-Bullying
    "women",
    "I am going to college today.",
    "I really enjoyed talking with you.",
    "Can you help me with my assignment?",
    "heyy kanha!i love you",

    # Threat
    "You better stay away from me.",
    "I will hurt you if you come near me.",
    "You will regret what you did.",

    # Harassment
    "Stop sending me unwanted messages.",
    "He keeps bothering me every day.",

    # Insult
    "You are such an idiot.",
    "That was a stupid thing to say.",

    # Religious Hate
    "I hate people because of their religion.",

    # Hate/Discrimination
    "That group should not be allowed to live here.",

    # Misogyny
    "Women are not capable of doing important jobs.",
    "women"
]


print("\n==============================================")
print("        UNSEEN MESSAGE TEST")
print("==============================================")

for message in test_messages:

    prediction, confidence = predict_message(message)

    print("\nMessage:", message)
    print("Prediction:", prediction)
    print(f"Confidence: {confidence:.2f}%")
    print("-" * 60)