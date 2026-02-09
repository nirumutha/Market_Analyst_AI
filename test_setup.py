import os
from dotenv import load_dotenv

# Load the keys from the .env file
load_dotenv()

print("--- SYSTEM CHECK ---")

if os.getenv("OPENAI_API_KEY"):
    print("✅ OpenAI Key found!")
else:
    print("❌ OpenAI Key MISSING.")

if os.getenv("SERPER_API_KEY"):
    print("✅ Serper Key found!")
else:
    print("❌ Serper Key MISSING.")

if os.getenv("APIFY_API_TOKEN"):
    print("✅ Apify Key found!")
else:
    print("❌ Apify Key MISSING.")
    
print("--------------------")