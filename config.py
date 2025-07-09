import os
from dotenv import load_dotenv

load_dotenv()  # <- YOU NEED THIS TO ACTUALLY LOAD .env VARIABLES

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
