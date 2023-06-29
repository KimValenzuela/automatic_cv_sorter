from dotenv import load_dotenv
import os
from home import main_screen

from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

def main():

    load_dotenv()
    #print(os.getenv('OPENAI_API_KEY'))

    main_screen()


if __name__ == '__main__':
    main();