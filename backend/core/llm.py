import os
from groq import AsyncGroq

# Retrieve the API key from the environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY is not set in the environment.")

# Initialize the async Groq client
groq_client = AsyncGroq(api_key=GROQ_API_KEY)
