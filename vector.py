'''database - look up relevant documents for context - load our docs '''

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os 


embeddings = OllamaEmbeddings(model="llama3.1:8b")

db_location = './chroma_db'

add_documents = not os.path.exists(db_location) 

if add_documents:
    documents = []
    ids = []

    # pass the page content metadata 