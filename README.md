# LangGraph + Ollama Llama-3.1 Examples

This repository contains demonstrable examples of using LangGraph with Ollama's Llama-3.1 model.

## Prerequisites

1. **Ollama installed and running**:

   ```bash
   # Install Ollama (if not already installed)
   # Visit: https://ollama.ai/download

   # Start Ollama service
   ollama serve

   # Pull the Llama-3.1 model (if not already done)
   ollama pull llama3.1:8b
   ```

2. **Python dependencies** (already installed):
   - langchain
   - langchain-community
   - langgraph
   - langchain-core

## Examples

### 1. Basic Conversational Agent (`api.py`)

A simple conversational agent with memory that maintains context across interactions.

**Features**:

- ✅ Conversation memory
- ✅ Context persistence
- ✅ Simple chat interface
- ✅ Graceful exit handling

**Run**:

```bash
python api.py
```

**What it does**:

- Creates a stateful conversation graph
- Maintains message history
- Provides a simple chat interface
- Handles exit commands gracefully

### 2. Advanced Multi-Node Agent (`advanced_langgraph_example.py`)

A sophisticated agent that classifies user input and routes to specialized handlers.

**Features**:

- 🎯 Input classification
- 🔀 Conditional routing
- 📝 Question answering
- 🛠️ Task assistance
- 🎨 Creative content generation
- 📊 Analysis capabilities
- ❓ Clarification requests

**Run**:

```bash
python advanced_langgraph_example.py
```

**What it does**:

- Automatically classifies user input
- Routes to appropriate specialized nodes
- Provides context-aware responses
- Demonstrates complex graph workflows

## Usage Examples

### Basic Chat Example

```
👤 You: What is Python?
🤖 Assistant: Python is a high-level, interpreted programming language...

👤 You: Can you tell me more about its applications?
🤖 Assistant: Certainly! Python has many applications including...
```

### Advanced Routing Example

```
👤 You: Help me write a function to calculate fibonacci numbers
🛠️ Task Help: I'll help you create a Fibonacci function. Here's a step-by-step approach...

👤 You: Write a poem about coding
🎨 Creative Response: In lines of code, dreams take flight...

👤 You: What are the pros and cons of microservices?
📊 Analysis: Let me break down the advantages and disadvantages of microservices...
```

## Graph Structure

### Basic Example

```
User Input → Chatbot Node → Continue/End Decision
      ↑                            ↓
      └── (if continue) ←←←←←←←←←←←←←←
```

### Advanced Example

```
User Input → Classify → Route to Handler → End
                ↓
         [Question Handler]
         [Task Handler]
         [Creative Handler]
         [Analysis Handler]
         [Clarification Handler]
```

## Key Features Demonstrated

1. **State Management**: Both examples show how to manage conversation state
2. **Memory**: Persistent conversation history using MemorySaver
3. **Conditional Logic**: Routing based on user input or conversation state
4. **Multiple Node Types**: Different specialized handlers for different tasks
5. **Error Handling**: Graceful handling of errors and edge cases
6. **Interactive CLI**: User-friendly command-line interfaces

## Troubleshooting

### Common Issues

1. **"Connection refused" error**:

   - Make sure Ollama is running: `ollama serve`
   - Check if the model is available: `ollama list`

2. **Model not found**:

   - Pull the model: `ollama pull llama3.1:8b`
   - Check model name in the code matches exactly

3. **Import errors**:
   - Ensure all dependencies are installed
   - Activate your virtual environment if using one

### Testing Connection

Both examples include connection testing. If you see "✅ Ollama connection successful!", you're ready to go!

## Extending the Examples

You can extend these examples by:

- Adding more specialized node types
- Implementing tool usage (web search, calculations, etc.)
- Adding more sophisticated routing logic
- Implementing different memory strategies
- Adding streaming responses
- Creating multi-agent workflows

## Performance Notes

- The examples use Llama-3.1:8b which provides good performance/quality balance
- For faster responses, consider using smaller models like `llama3.1:3b`
- For better quality, consider using larger models like `llama3.1:70b` (requires more resources)
