import lancedb
from langchain.embeddings.openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
uri = "data/sample-lancedb"
db = lancedb.connect(uri)

def create_table(table_name, data):
    table = db.create_table(name=table_name, data=data)
    return table

def query_db(query, documents, table):
    docsearch = db.from_documents(documents, embeddings, connection=table)
    return docsearch


# def delete_collection(name_collection):
#     client.delete_collection(name = name_collection)


# def add_new_document(name_collection, ids, document):
#     collection = client.get_collection(name = name_collection, embedding_function= OpenAIEmbeddings())
#     collection.add(
#         ids = ids, 
#         documents = document
#     )

# def get_cvs(name_collection, query_text):
#     collection = client.get_collection(name = name_collection, embedding_function= OpenAIEmbeddings())
#     results = collection.query(
#         query_texts=query_text,
#         n_results=5,
#         #where_document = {'$contains': 'skill'} # aqui se podria filtrar por skills
#     )
#     return results
    


