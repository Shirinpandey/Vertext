"""
Simple test to verify Ollama connection
"""

from langchain_ollama import OllamaLLM


def test_connection():
    try:
        llm = OllamaLLM(model="llama3.1:latest")
        print("🔄 Testing Ollama connection...")
        response = llm.invoke("Say hello in one word.")
        print(f"✅ Success! Response: {response}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    test_connection()
