from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline
import os
import streamlit as st

os.environ["HF_HOME"] = "F:/Python3/AA_Practice/genai/TinyLlama"
llm = HuggingFacePipeline.from_model_id(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", task="text-generation")
model = ChatHuggingFace(llm=llm)

chat_template = ChatPromptTemplate([
    ('system', 'You are helpful customer agent'),
    MessagesPlaceholder(variable_name='chat_history'), # it needs for  chatbot to first load the previous chat history from any database and then get the contxt of new human message
    ('human', "{query}")
])
chat_history = ["Human: I want to return the product","AI: Yes we are processing"]
prompt = chat_template.invoke({'chat_history':chat_history, 'query': 'where is my refund'})
print(prompt)
result = model.invoke(prompt)
print(result.content)