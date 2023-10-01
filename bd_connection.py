from langchain.embeddings.openai import OpenAIEmbeddings
import chromadb


client = chromadb.PersistentClient(path="chroma_data")
client.get_version()

def create_collection():
    client.create_collection(
        name = "cvs",
        embedding_function = OpenAIEmbeddings(),
        get_or_create = True
    )


def delete_collection(name_collection):
    client.delete_collection(name = name_collection)


def add_new_document(name_collection, ids, document):
    collection = client.get_collection(name = name_collection, embedding_function= OpenAIEmbeddings())
    collection.add(
        ids = ids, 
        documents = document
    )

def get_cvs(name_collection, query_text):
    collection = client.get_collection(name = name_collection, embedding_function= OpenAIEmbeddings())
    results = collection.query(
        query_texts=query_text,
        n_results=5,
        #where_document = {'$contains': 'skill'} # aqui se podria filtrar por skills
    )
    return results
    


