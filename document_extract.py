from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool
from langchain.docstore.document import Document

embeddings = OllamaEmbeddings(model="nomic-embed-text")  
# take information from the documents here instead of the list here
texts = [
    "Claude is best for reasoning, summarization, and coding assistance.",
    "GPT-4 is strong at creativity, complex reasoning, and handling nuanced queries.",
    "Gemini is optimized for research, large-scale analysis, and multimodal tasks.",
]
docs = [Document(page_content=t) for t in texts]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
pages_split = text_splitter.split_documents(texts)

vectorstore = FAISS.from_texts(texts, embedding=embeddings)
retriever = vectorstore.as_retriever(
    search_type="similarity", search_kwargs={"k": 5}
)

@tool
def retriver_tool(query:str)-> str:
    '''A tool searches and returns the information from the data provided'''

    docs = retriever.invoke(query)
    if not docs:
        return 'I did not find any relevant information'
    
    result = []

    for i,doc in docs:
        result.append(f"Document {i+1}: {doc.page_content}")
    
    return '/n'.join(result)
