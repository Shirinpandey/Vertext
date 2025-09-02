# Vertext

A Language Model interaction tool using Ollama, LangChain and Langgraph.

## Prerequisites

### Ollama Setup
1. Install Ollama
   - Visit [Ollama Download Page](https://ollama.ai/download)
   - Follow installation instructions for your platform

2. Start Ollama Service
   ```bash
   ollama serve
   ```

3. Pull Required Model
   ```bash
   ollama pull mistral
   ```

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/vertext.git
   cd vertext
   ```

2. Install Python dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Requirements

The following packages are required:
- langchain
- langchain-ollama
- langchain-chroma
- langgraph

These can be installed using the provided `requirements.txt` file.

## Usage

Run the main script:
```bash
python main.py
```

Follow the prompts to interact with the language model.

## Notes
- Ensure Ollama service is running before starting the application
- Make sure you have sufficient system resources for running the model