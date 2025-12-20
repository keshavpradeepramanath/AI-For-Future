import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['HF_TOKEN']=os.getenv('HF_TOKEN')
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")



##Setup Streamlit app
st.title('Conversational RAG with PDF loader and history')
st.write('Upload PDFs and chat with the content')


##Input GRoq API Key
api_key = st.text_input('Enter your Groq API Key',type=password)


##Check if Grqo API key is provided
if api_key:
    llm = ChatGroq(groq_api_key = api_key, model_name="Gemma2-9b-It")

    ##Chat Interface
    session_id =st.text_input("Session ID", value="Default Session")



    if 'store' not in st.session_state:
        st.session_state.store ={}

    uploaded_files = st.uploader('Choose a PDF File',type="pdf", accept_multiple_files=False)    
    ##Process uplaoded files

    if uploaded_files:
        documents =[]
        for uploaded_file in uplaoded_files:
            temppdf = f"./temp.pdf"
            with open(temppdf,"wb") as file:
                file.write(uploaded_file.getvalue())
                file_name= uploaded_file.name

            loader = PyPDFLoader(temppdf)
            docs = loader.load()
            docuemts.extend(docs)    

        ## Split and create embeddings  

        text_splitter = RecursiceCharacterTextSplitter(chunk_size=200,chunk_overlap=75)
        splits = text_splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(documents=splits,embedding=embeddings)
        retriever = vectorstore.as_retriever()

        contextualize_q_system_prompt = (
            "Given chat history and latest user question, "
            "which might reference context in chat history"
            "formulate standdard question that can be understood"
            "without chat history.Do not answer the question"
            "just re-formulate it if needed,otherwise return it as it "
        )

        contextualize_q_prompt = ChatPromptTemnplate.from_messages(
            [
                ("system",contextualize_q_system_prompt),
                MessagePlaceholder("chat_history"),
                ("human","{input}")
            ]
        )

        history_aware_retriever= create_history_aware_retriever(llm,retriever,contextualize_q_prompt)

        ##Answer Question

        system_prompt= (
            "You aer an assistanr to answer questions"
            "use the following peices of retrieved context to answer"
            "If you dont know the answer, tell that you dont know"
            "Use 3 sentenses max"
            "\n\n"
            "{context}"
        )

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",system_prompt),
                MessagePlaceholder("chat_history"),
                ("human","{input}")
            ]
        )

        question_answer_chain= create_stuff_document_chain(llm,qa_prompt)
        rag_chain= create_retrieval_chain(history_aware_retriever,question_answer_chain)


        def get_session_history(session:str)->BaseChatMessageHistory :
            if session_id not in st.session_state.store:
                st.session_state.store[session_id]=ChatMessageHistory()
            return st.session_state.store[session_id]

        conversational_rag_chain=RunnableWithMessageHistory(
            rag_chain,get_session/-history,
            input_messages_key = "input",
            history_messages_key = "chathistory",
            output_messages_key = "answer"
        )

        user_input = st.text_input("Your question")
        if user_input:
            session_history = get_session_history(session_id)
            response = conversational_rag_chain.invoke(
                {"input":user_input},
                config= {
                    "configurable":{"session_id":session_id}
                }
            )

            st.write(st.session_state.store)
            st.success("Assistant: ",response['answer'])
            st.write("Chat History: ", session_history.messages)

else:
    st.warning('Please endter the Groq API key')
