from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os

from dotenv import load_dotenv

load_dotenv()

##Langsmith tracking
os.environ['LANGCHAIN_API_KEY']= os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2']='true'
os.environ['LANGCHAIN_PROJECT']='Simple QnA chatbot with Ollama'

##Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ('system',"You are a useful assistant in answering questions"),
        ('user',"Question:{question}")
    ]
)


def generate_reposnse(question,engine, temperature, max_token):
    
    llm = Ollama(model = engine)
    output_parser = StrOutputParser()
    chain = prompt |llm| output_parser
    answer = chain.invoke({'question':question})
    return answer



##Drop down to select models
llm= st.sidebar.selectbox('Select an OpenAI model',['llama3.2','llama3','gemma:2b'])

##Adjust temperature and max token
temperature = st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens",min_value=50,max_value=200,value=100)


##Main interface
st.write('Go ahead and ask any question')
user_input=st.text_input('You:')

if user_input:
    response= generate_reposnse(user_input,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write('Please provide a question')    

