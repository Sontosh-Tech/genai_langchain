from langchain_ollama import OllamaLLM
import os

# 1. Prevent the OpenAI client from trying to reach the cloud
os.environ["OPENAI_API_KEY"] = "ollama"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"

# 2. Initialize the Ollama LLM
# Note: LangChain's OllamaLLM usually connects to 11434 by default.
ollm = OllamaLLM(
    model="llama3.2",
    temperature=0.1,
    base_url="http://localhost:11434"
)

# Test the connection
try:
    response = ollm.invoke("what is the UA-IRAN conflict?")
    print(response)
except Exception as e:
    print(f"Still hitting an error: {e}")