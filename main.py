from langchain_ollama import OllamaLLM
from classify_tool import classify
from langchain.agents import initialize_agent, Tool

model = OllamaLLM(model="llama3.1:latest", temperature=0)
classification_tool = Tool(
    name="Classify",
    func=classify,
    description="Classifies text into Coding, Writing, Research, or Summarization"
)
agent = initialize_agent(
    tools=[classification_tool],
    llm=model,
    agent="zero-shot-react-description"
)

while True:
    user_input = input("Enter your prompt (or 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    try:
        output = agent.invoke({"input": user_input})
        print("AI Output:", output['output_text'] if isinstance(output, dict) else output)
    except Exception as e:
        print("Error:", e)
