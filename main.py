from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate


model = OllamaLLM(model="llama3.1:8b")
template = '''
You are a helpful assistant that translates {word} into French.

'''
prompt = ChatPromptTemplate.from_template(template)

# passing prompt in model
chain = prompt | model 

while True:
    print('-'*50\n)
    question = input("Enter your prompt (q to quit): ")
    if question.lower() == 'q':
        break
    result = chain.invoke({'word': question})
    print(result)