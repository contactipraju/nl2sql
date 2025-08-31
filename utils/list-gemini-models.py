import google.generativeai as genai

from config import GEMINI_API_KEY

# Configure your API key
genai.configure(api_key=GEMINI_API_KEY)

for m in genai.list_models():
	if "generateContent" in m.supported_generation_methods:
		print(f"Model: {m.name}, Supported Methods: {m.supported_generation_methods}")