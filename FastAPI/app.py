from fastapi import fastapi
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from dotnev import load_dotenv
from langchain_community.llms import Ollama


load_getenv()
os.environ['OPEN_API_KEY'] = os.getenv('OPENAI_API_KEY')


app = FastAPI(
    title =" Langschain Server",
    version = "1.0",
    description="Simple API Server"
)

add_routes (
    app,
    ChatOpenAI(),
    path ="/openai"
)

model = ChatOpenAI()
llm = Ollama(model = "gemma:2b")

prompt1 = ChatPromptTemplate.from_template("Write a essay on {topic} with 100 words")
prompt2 = ChatPromptTemplate.from_template("Write a poem on {topic} with 100 words")

add_routes (
    app,
    prompt1,model,
    path ="/essay"
)

add_routes (
    app,
    prompt2,llm,
    path ="/poem"
)


if __name__=="__main__" :
    uvicorn.run(app,host="localhost",port=8000)