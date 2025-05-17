import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key - ensure this name matches what's in your .env file
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Add this debug print to verify loading
print(f"Config loaded. API key exists: {OPENROUTER_API_KEY is not None}")