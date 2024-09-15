import json
import pandas as pd
import sys
import re
import requests
import os
import numpy as np
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
from openai import AzureOpenAI


client = AzureOpenAI(
  azure_endpoint = "xxx", 
  api_key=os.getenv("xxx"),  
  api_version="2024-02-15-preview"
)

# Opening JSON file
f = open('json_data.json')

# returns JSON object as
# a dictionary
data = json.load(f)

transcript = "Operator: Good morning, thank you for calling the auto insurance company, my name is John, how can I assist you today?\nCustomer: Yes, hi, I just noticed a dent on the side of my car and I have no idea how it got there. There were no witnesses around and I'm really frustrated.\nOperator: I'm sorry to hear that, I understand how frustrating it can be. Can you please provide me with your name and policy number so I can look up your account?\nCustomer: Yes, I’m Mario Rossi and the policy number is 123456.\nOperator: Thank you Mr. Rossi, let me take a look. I see that you've called earlier today, was there an issue with that call?\nCustomer: Yes, I was on hold for over an hour and the issue was not resolved. I'm really not happy about it.\nOperator: I'm sorry about that, let me assure you that we value your time and we'll do our best to assist you today. As for the dent on your car, I'd like to inform you that our policy does cover accidental damage like this. I can help you file a claim and connect you with one of our trusted repair shops in your area. Would you like me to proceed with that?\nCustomer: Yes, please. That would be great.\nOperator: Thank you for your cooperation. I'm now processing your claim and I'll be sending you an email with the next steps to follow. Please let me know if you have any other questions or concerns.\nCustomer: Thank you, I appreciate your help.\nOperator: You're welcome. Have a great day!\n\n\n"

st.set_page_config(
    page_title="Home",
    page_icon="🚗",
)


st.header("Welcome to Car Insurance management portal🚗")


st.subheader('Transcript Case #37294810', '📞')

st.text(transcript)


def create_ticket(data):
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=[
            {"role": "system", "content": "You are a helpful  assistant."},
            {"role": "user", "content": f"""Generate a response email to the transcript below, notifying the customer that the ticket has been created and apologizing if it was complaining. The name of the customer is {data['name']}.
            Transcript: {transcript}""" },
        ]
    )
    return response.choices[0].message.content
    


def generate_email(transcript):
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=[
            {"role": "system", "content": "You are a helpful  assistant."},
            {"role": "user", "content": f"""Generate a response email to the transcript above, notifying the customer that the ticket has been created and apologizing if it was complaining. The name of the customer is {data['name']} and the policy number is {data['policy_number']}.
            Transcript: {transcript}""" },
        ]
    )
    return response.choices[0].message.content
    
    
def improvement(data):
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=[
            {"role": "system", "content": "You are a helpful  assistant."},
            {"role": "user", "content": f"""Elaborate a list of remediations to get to the following improvement: {data['contact_center_improvement']}.
            Transcript: {transcript}""" },
        ]
    )
    return response.choices[0].message.content

    
    
if st.button('Create Ticket'):
    ticket_number = np.random.randint(1,1000000)
    st.write(f'Your ticket has been created with number {ticket_number}. Customer and incident manager will be notified shortly')

    
if st.button('Generate email'):
    st.write(generate_email(transcript))
    
if st.button('Improve customer service quality'):
    st.write(improvement(data))
