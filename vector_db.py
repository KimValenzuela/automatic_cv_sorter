from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import TensorflowHubEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate

#vectordb = None

def loader_docs(model_embed):
    embedding = OpenAIEmbeddings(
        model = model_embed,
        chunk_size = 1000,
    )
    loader = PyPDFDirectoryLoader(path='cv_files/', glob='*.pdf')
    docs = loader.load()
    vectordb = Chroma.from_documents(
        documents = docs, 
        embedding = embedding,
        persist_directory = 'bd'
    )
    vectordb.persist()

    return vectordb

def similarity_search(text, vectordb):
    
    response = vectordb.similarity_search_with_score(
        query = text,
        k = 4
    )

    cvs_list = []
    source_set = set() 

    for resp in response:
        cvs = {}
        source = resp[0].metadata['source'].split("/")
        print("SOURCE SIN SPLIT: ", resp[0].metadata['source'])
        source = source[1] if len(source) > 1 else source[0]  
        print("source: ", source)
        if source not in source_set:  
            cvs['source'] = source
            print("score: ", resp[1])
            cvs['score'] = resp[1]
            cvs_list.append(cvs)
            source_set.add(source)  

    return cvs_list




def candidate_question(pdf, query, model, temperature, model_embed):
    llm = OpenAI(
        model = model,
        temperature = temperature
    )

    knowledge_base = pdf_questions(pdf, model_embed)
    docs = knowledge_base.similarity_search(query = query)
    chain = load_qa_chain(llm, chain_type='stuff')

    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=query)
    
    return response


def pdf_questions(pdf, model_embed):
    pdf_reader = PdfReader('cv_files/' + pdf)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()

    text_splitter = CharacterTextSplitter(
        separator = '\n',
        chunk_size = 1000,
        chunk_overlap = 200
    )
    chunks = text_splitter.split_text(text)
    embedding = OpenAIEmbeddings(model = model_embed)
    knowledge_base = FAISS.from_texts(chunks, embedding)
    
    return knowledge_base

def context_model(template, query):
    template_query = template + """
    Pregunta: {query_user}
    Respuesta:""" 
    prompt_tem = PromptTemplate(input_variables=['query_user'], template=template_query)
    prompt_value = prompt_tem.format(query_user = query)

    return prompt_value
    
def job_skills(job_description, model, temperature):
    template_query = """
    Dicta las habilidades necesarias que debe tener una persona para poder tener éxito en un puesto de trabajo con la siguiente descripción: {description_job}.
    Respuesta: El candidato debe presentar las siguientes habilidades: 
    """
    prompt_tem = PromptTemplate(input_variables=['description_job'], template=template_query)
    prompt_value = prompt_tem.format(description_job=job_description)

    llm = OpenAI(
        model = model,
        temperature=temperature
    )

    response = llm(prompt_value)

    return response

