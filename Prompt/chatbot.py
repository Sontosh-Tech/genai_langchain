from langchain_core.prompts import PromptTemplate, load_prompt
from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage # this is for labeling the chat users
import os
import streamlit as st

os.environ["HF_HOME"] = "F:/Python3/AA_Practice/genai/TinyLlama"
llm = HuggingFacePipeline.from_model_id(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", task="text-generation")
model = ChatHuggingFace(llm=llm)

chat_history = [SystemMessage(content="Thanks for choosing me ! Plese go ahead...")]

while True:
    user_input = input("you: ")
    chat_history.append(HumanMessage(content=user_input))
    if user_input == 'exit':
        break
    result = model.invoke(user_input)
    chat_history.append(AIMessage(content=result.content))
    print("AI: ", result.content)

print(chat_history)