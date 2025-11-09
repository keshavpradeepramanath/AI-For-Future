import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


import os
from dotenv import load_dotenv

load_dotenv()


##Langsmith tracking
os.environ['LANGCHAIN_API_KEY']= os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2']='true'
os.environ['LANGCHAIN_PROJECT']='Simple QnA chatbot with OpenAI'


##Prompt Template

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant.Please answer the queries"),
        ("user","Question : {question} ")
    ]
)


def generate_reposnse(question,api_key,llm, temperature, max_token):
    openai.api_key = api_key
    llm = ChatOpenAI(model = llm)
    output_parser = StrOutputParser()
    chain = prompt |llm| output_parser
    answer = chain.invoke({'question':question})
    return answer



##Title of the app

st.title('Enhanced QnA Chatbot with OpenAI')

##Sidebar settings
st.sidebar.title('Settings')
api_key=st.sidebar.text_input('Enter your API Key',type='password')


##Drop down to select models
llm= st.sidebar.selectbox('Select an OpenAI model',['gpt-4o','gpt-3.5-turbo','gpt-4-turbo'])

##Adjust temperature and max token
temperature = st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens",min_value=50,max_value=200,value=100)


##Main interface
st.write('Go ahead and ask any question')
user_input=st.text_input('You:')

if user_input:
    response= generate_reposnse(user_input,api_key,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write('Please provide a question')    



