import streamlit as st
import openai
import os
import openai
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI
from langchain.llms import AzureOpenAI
from pypdf import PdfReader
from langchain.vectorstores.faiss import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader

import openai

import os
from langchain_openai import AzureOpenAI


os.environ["AZURE_OPENAI_API_VERSION"] = "2024-02-15-preview"
os.environ["AZURE_OPENAI_ENDPOINT"] = "xxx"
os.environ["AZURE_OPENAI_API_KEY"] = "xxx"
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"] = "gpt-4o"



llm = AzureChatOpenAI(
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
)



embeddings = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-3-large"
)

st.set_page_config(
    page_title="Home",
    page_icon="👨‍⚕️",
)


st.header("Welcome to Biology Smart Search👨‍⚕️")

with st.sidebar.expander(" 🛠️ Settings ", expanded=False):
    
    FILE = st.selectbox(label='File', options=['biology.pdf'])



if FILE:
    loader = PyPDFLoader(FILE)
    pages = loader.load_and_split()
    faiss_index = FAISS.from_documents(pages, embeddings)
    retriever = faiss_index.as_retriever()

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

query = st.text_area("Ask a question about the document")

if query:
    button = st.button("Submit")
    if button:
        response = rag_chain.invoke({"input": "what are the benefit of live cell microscopy??"})
        st.write(response["answer"])