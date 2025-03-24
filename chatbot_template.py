from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline
import os
import streamlit as st

os.environ["HF_HOME"] = "F:/Python3/AA_Practice/genai/TinyLlama"
llm = HuggingFacePipeline.from_model_id(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", task="text-generation")
model = ChatHuggingFace(llm=llm)

chat_template = ChatPromptTemplate([
    ('system', 'You are helpful {domain} expert'),
    ('human', "Explain in simple terms , what is {topic}")
])
prompt = chat_template.invoke({'domain':'cricket', 'topic': 'dusra'})
result = model.invoke(prompt)
print(result.content)