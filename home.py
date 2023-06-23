import streamlit as st
from handle_pdfs import read_pdf
from bd_connection import query_db

def home():
    st.set_page_config(page_title = 'CVs Ask')
    st.header('CVs Ask')

    upload_files = st.file_uploader('Upload your CV', type='pdf', accept_multiple_files=True)
    
    if upload_files:
        st.write("Uploaded documents!")

        for file in upload_files:
            read_pdf(file)

        description = st.text_area("Insert a job description: ")
        #tags = st.sidebar.text_input("Insert the skills you are looking for: ")
    
       
        if description:
            response = query_db(description)
            st.write(response)

    # if st.button("Upload documents", use_container_width=True):
    #     cargar_documentos()

    # if st.button("Consult documents", use_container_width=True):
    #     consultar_documentos()

def cargar_documentos():
    upload_files = st.file_uploader('Upload your CV', type='pdf', accept_multiple_files=True)
    
    if upload_files:
        st.write("Uploaded documents!")

        for file in upload_files:
            read_pdf(file)

def consultar_documentos():
    description = st.text_area("Insert a job description: ")
    #tags = st.sidebar.text_input("Insert the skills you are looking for: ")
    
    if st.button("Consult"):
        
        if description:
            response = query_db(description)
            st.write(response)

        # if tags:
        #     st.write(description)

