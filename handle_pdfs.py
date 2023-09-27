from PyPDF2 import PdfReader
from bd_connection import create_table
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader


def read_pdf(pdf):
    loader = PyPDFLoader(pdf)
    pages = loader.load_and_split()
    
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    make_chunks(text)


def make_chunks(text):
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = text_splitter.split_text(text)
    create_table(chunks)
    