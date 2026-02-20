from google import genai

# Pass the string directly as the api_key
client = genai.Client(api_key="AIzaSyBvNgRnSw0Y1fG6s3bWdvGpHYnQE1X_LeU")

for m in client.models.list():
    print(f"✅ Found Model: {m.name}")
