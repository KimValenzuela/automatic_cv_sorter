from dotenv import load_dotenv
import os
from home import home

from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI



def main():
    load_dotenv()
    print(os.getenv('OPENAI_API_KEY'))

    home()

    

        # chunks
        

        


        # user_question = st.text_input("Ask a question: ")
        # if user_question:
        #     docs = knowledge_base.similarity_search(user_question)
            
        #     llm = OpenAI()
        #     chain = load_qa_chain(llm, chain_type="stuff")
        #     response = chain.run(input_documents = docs, question = user_question)

        #     st.write(response)


if __name__ == '__main__':
    main();