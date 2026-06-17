import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the ChatGroq client
llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct", api_key=groq_api_key
)
