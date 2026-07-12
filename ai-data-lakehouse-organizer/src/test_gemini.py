import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print(f"API Key starts with: {api_key[:10]}...")
print(f"API Key ends with: {api_key[-6:]}")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="Say Hello"
)

print("\nResponse:")
print(response.text)