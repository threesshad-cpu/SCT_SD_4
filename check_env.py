import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Print current location to make sure we are in C:\t4
print(f"📍 Current Directory: {os.getcwd()}")

# 2. Check if .env file actually exists on the hard drive
env_file = Path(".env")
if env_file.exists():
    print("✅ .env file found.")
else:
    print("❌ ERROR: .env file NOT FOUND in this folder. Make sure it isn't named '.env.txt'")

# 3. Try to load it
loaded = load_dotenv()
print(f"📡 load_dotenv() success: {loaded}")

# 4. Check the key
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    print(f"🔑 Key found! Starts with: {api_key[:4]}")
else:
    print("❌ Key still missing. Double-check the spelling of GEMINI_API_KEY in the file.")