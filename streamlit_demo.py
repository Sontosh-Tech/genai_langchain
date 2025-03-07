#from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline
#from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM, pipeline
import os
import streamlit as st

#model_path = "F:/Python3/AA_Practice/genai/TinyLlama/hub/models--TinyLlama--TinyLlama-1.1B-Chat-v1.0/snapshots/fe8a4ea1ffedaf415f4da2f062534de366a451e6/config.json"
os.environ["HF_HOME"] = "F:/Python3/AA_Practice/genai/TinyLlama"
llm = HuggingFacePipeline.from_model_id(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", task="text-generation")
model = ChatHuggingFace(llm=llm)
st.header("AI Demo with Langchain")
prompt = st.text_input("Enter your prompt: ")
if st.button("Summarize"):
    result = model.invoke(prompt)
    st.write(result.content)

