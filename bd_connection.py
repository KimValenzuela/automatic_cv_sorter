from langchain.vectorstores import Chroma
from langchain.embeddings import TensorflowHubEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings

db = ""

def save_docs_db(docs):
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(docs, embeddings)
    
def query_db(query):
    docs = db.similarity_search_with_score(query)
    return docs

