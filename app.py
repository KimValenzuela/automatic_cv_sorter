from dotenv import load_dotenv, set_key
from home import main_screen
import os

def main():
    os.environ['OPENAI_API_KEY'] = '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'
    #set_key(".env", "OPENAI_API_KEY", "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")
    load_dotenv()
    API_KEY = os.getenv("OPENAI_API_KEY")
    print(API_KEY)
    main_screen()

if __name__ == '__main__':
    main();