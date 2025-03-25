from typing import TypedDict, Annotated, Optional, Literal
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline
import os
import streamlit as st

os.environ["HF_HOME"] = "F:/Python3/AA_Practice/genai/TinyLlama"
llm = HuggingFacePipeline.from_model_id(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", task="text-generation")
model = ChatHuggingFace(llm=llm)

class Review(TypedDict):
    key_themes: Annotated[list[str], "Write down all the key themes discussed in the review in a list"]
    summary: Annotated[str, "A brief summary of the review"]
    sentiment: Annotated[str, "Returns sentiment of the review either positive , negative or neutral"]
    sentiment_with_literal: Annotated[Literal["pos", "neg"], "Returns sentiment of the review either positive , negative or neutral"]
    pros: Annotated[Optional[list[str]], "write down all the pros inside a list"]
    cons: Annotated[Optional[list[str]], "write down all the cons inside a list"]


structured_model = model.with_structured_output(Review)

review1 = "The Realme P1 Speed is a good device for the money. It is now equipped with an enticing OLED panel, 120Hz refresh rate support and performance through MediaTek Dimensity 7300 SoC. It has a large 5000mAh battery and supports 45W charging, so it fits power users."
result = structured_model.invoke(review1)
print(result)