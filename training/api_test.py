import requests

url = "http://127.0.0.1:5000/predict"

messages = [
    "I am going to college today.",
    "You better stay away from me.",
    "You are such an idiot.",
    "Women cannot do important jobs."
]

for message in messages:

    response = requests.post(
        url,
        json={"text": message}
    )

    result = response.json()

    print("\nMessage:", message)
    print("Category:", result["category"])
    print("Confidence:", result["confidence"])
    print("-" * 50)