from google import genai

client = genai.Client(api_key="GOOGLE_API_KEY")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)


curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H "Content-Type: application/json" \
  -H "X-goog-api-key: AIzaSyBG8kAm64s9dHoH7qnPgulaunkI_eBSiyA" \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "how do I load env variables in python?"
          }
        ]
      }
    ]
  }'