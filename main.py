from langchain_ollama import OllamaLLM
from classify_tool import classify
from langchain.agents import initialize_agent, Tool

model = OllamaLLM(model="llama3.1:latest", temperature=0)# brain is llama 3.1
#temp = 0 gives more precise answers + more focused ones

classification_tool = Tool(
    name="Classify",
    func=classify,
    description="Classifies text into Coding, Writing, Research, or Summarization"
)
# a tool the agent can use -> tools job -> classify the user input

agent = initialize_agent(
    tools=[classification_tool],
    llm=model,
    agent="zero-shot-react-description" # ai looks at description of each tool
    # and decides which one to use based on user input without training examples
)
# building the agent here -> agent = llama brain + available tools


while True: # keeps asking for user input until 'exit' is typed
    
    user_input = input("Enter your prompt (or 'exit' to quit): ")
    if user_input.lower() == "exit":
        break
    try:
        output = agent.invoke({"input": user_input}) # sends your input to agent
        # agent decides if it shoudl answer or call claissify tool

        # confused abt this line???????????????
        print("AI Output:", output['output_text'] if isinstance(output, dict) else output)
    except Exception as e:
        print("Error:", e)
