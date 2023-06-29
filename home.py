import streamlit as st
from yaml.loader import SafeLoader
import yaml
from PIL import Image
from pathlib import Path
from vector_db import loader_docs
from vector_db import similarity_search, candidate_question, job_skills
import webbrowser

####################################################################
#####################       Parameters       #######################
####################################################################

__version__ = "0.0.1"
app_name = 'CV-Job Matcher'
models = ['text-davinci-003','text-curie-001', 'gpt-3.5-turbo','gpt-4',] #put here models available
embed_models = ['text-embedding-ada-002']

#we read prompt tasks from yaml file
with open('prompts.yml') as f:
    prompts = yaml.load(f, Loader=SafeLoader)

im = Image.open("images/ey2.png")
st.set_page_config(page_title=app_name, page_icon=im, layout="centered", initial_sidebar_state="auto", menu_items=None)
ss = st.session_state #this variable saves params of all widgets, the name of each param is the same that key value in widgets
print(ss)

###################################################################
#####################       Functions       #######################
###################################################################

def app_spacer(n=2, line=False, next_n=0):
    """Function that create spaces between lines.

    Parameters:
        n (int): 
        line (boolean): 
        next_n (int): 

    Returns:
        None
    """

    for _ in range(n):
        st.write('')
    if line:
        st.tabs([' '])
    for _ in range(next_n):
        st.write('')

def app_info():
    """Function that fill the sidebar with information about author.

    Parameters:
        None

    Returns:
        None
    """

    st.markdown(f"""
        # {app_name}
        version: {__version__}
        
        A Job - Employee matcher system built using LangChain and ChatGPT.
        """)
    app_spacer(1)
    st.write("Made by [Kim Valenzuela](https://github.com/KimValenzuela/). Supported by EY-Chile Training Team.", unsafe_allow_html=True)
    app_spacer(1)
    st.markdown("""
        This proyect was built as example for a training session framed in the EY-Python Chile Hackathon 2023.
        """)
    app_spacer(1)
    st.markdown('')

def upload_pdfs():
    """Function that allows to get pdf files given by user.

    Parameters:
        None

    Returns:
        None
    """
    st.write('### Please upload your CV documents here.')
    upload_files = st.file_uploader('Upload your CV', key='pdf_file',type='pdf', accept_multiple_files=True)

    #Here ss['pdf_file'] is a list of metadata of pdf given by user.
        
    if upload_files:
        #print(ss['pdf_file'])
        st.write("Uploaded documents!")

        for file in upload_files:
            save_folder = 'cv_files/'
            save_path = Path(save_folder, file.name)
        
            with open(save_path, mode = 'wb') as w:
                w.write(file.getvalue())

def consultar_documentos():
    #ToDo: DOCSTRING
    """ XXXXXXXXXXXXXXXXXXXXXXXX

    Parameters:
        None

    Returns:
        None
    """

    description = st.text_area("Insert a job description: ")
    #tags = st.sidebar.text_input("Insert the skills you are looking for: ")
    
    if st.button("Consult"):
        
        if description:
            model = ss['model']
            model_embed = ss['model_embed']
            temperature = ss['temperature']
            vectordb = loader_docs(model_embed)
            response = similarity_search(description, vectordb)
            skills = job_skills(description, model, temperature)
            st.header('Skills for the position')
            st.write(skills)
            st.header('Candidates')
            col1, col2 = st.columns(2)
            for res in response:
                # url = f"[Link](file:///home/kim/Escritorio/Pyday/Proyecto2/automatic_cv_sorter/cv_files/CV_Kimberly_Valenzuela.pdf)"
                # st.markdown(url, unsafe_allow_html=True)
                with col1:
                    st.write(res['source'])
                with col2:
                    st.write(res['score'])

        # if tags:
        #     st.write(description)

def app_set_temperature():
    """Function that allows to set temperature to a model.

    Parameters:
        None

    Returns:
        None
    """

    st.slider('Temperature', 0.0, 1.0, 0.0, 0.01, key='temperature', format='%0.2f')
    print(ss['temperature'])
    #ss['temperature'] = 0.0

def app_llm_model():
    """Function that allows to select the model using a list of models setted above (see parameters section).

    Parameters:
        None

    Returns:
        None
    """

    st.selectbox('OpenAI model', models, key='model')
    st.selectbox('embedding model', embed_models, key='model_embed')
    print(ss['model'])
    print(ss['model_embed'])

def app_task_names():
    """Function that allows to select the task used by the model. The tasks template are setted in a yaml file (see parameters section).

    Parameters:
        None

    Returns:
        None
    """

    st.selectbox('Task prompt template name', prompts['tasks'], key='task_name')

def app_task_modifier():
    """Function that allows to modify the task given to the model. The tasks template are setted in a yaml file (see parameters section).

    Parameters:
        None

    Returns:
        None
    """
    x = ss['task_name']
    st.text_area('Task prompt', prompts['tasks'][x], key='task')

def app_question():
    """Function that allows to select a document and put a question to this document.

    Parameters:
        None

    Returns:
        None
    """

    st.write('### Ask questions to a candidate')
    file_names=[file.name for file in ss['pdf_file']]
    file_select = st.selectbox('Select document to ask questions', file_names, key='file_names')
    disabled = False
    query = st.text_area('question', key='question', height=100, placeholder='Enter question here', help='', label_visibility="collapsed", disabled=disabled)
    if query:
        model = ss['model']
        model_embed = ss['model_embed']
        temperature = ss['temperature']
        print('File Select: ', file_select)
        response = candidate_question(file_select, query, model, temperature, model_embed)
        st.write(response)
    


def app_output():
    """Function that print the output of the model below the question area.

    Parameters:
        None

    Returns:
        None
    """
    output = ss.get('output','')
    st.markdown(output)

def app_ask_question():
    """Function that creates buttons to send the answer and clear the answer. If get answer is clicked, we can call the model.

    Parameters:
        None

    Returns:
        None
    """	

    c1,c2= st.columns([2,2])
    disabled = False #we can set True if model is working or something like that
    if c2.button('clear_answer',disabled=disabled,type='primary',use_container_width=True):
        ss['output']=''
    if c1.button('get answer', disabled=disabled, type='primary', use_container_width=True):
        question = ss.get('question','')
        temperature = ss.get('temperature', 0.0)
        task = ss.get('task')
        with st.spinner('preparing answer'):
            resp=''
            #Here we can put the model including the task, the temperature, etc
        
        q = question.strip()
        a = resp['text'].strip()
        ss['answer'] = a
        output_add(q,a)

def output_add(q,a):
    """Function that allows to add question and aswers to the output.

    Parameters:
        None

    Returns:
        None
    """	
    if 'output' not in ss: ss['output'] = ''
    new = f'#### {q}\n{a}\n\n'
    ss['output'] = new + ss['output']

###################################################################
######################       LAYOUT       #########################
###################################################################

def main_screen():
    """Function that creates the frontend layout.

    Parameters:
        None

    Returns:
        None
    """	

    #TITLE
    st.title(f"📝 :female-office-worker: :office_worker:  {app_name}")

    #SIDEBAR
    with st.sidebar:
        app_info()
        app_spacer(2)
        with st.expander('Advanced Parameters'):
            app_llm_model()
            app_set_temperature()
            app_task_names()
            app_task_modifier()

    #MAIN PAGE
    upload_pdfs()
    consultar_documentos()
    app_question()
    app_ask_question()
    app_output()

#home()