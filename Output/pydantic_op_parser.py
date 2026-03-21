from typing import TypedDict, Annotated, Optional, Literal
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
import os
import streamlit as st

os.environ["HF_HOME"] = "F:/Python3/AA_Practice/genai/TinyLlama"
llm = HuggingFacePipeline.from_model_id(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", task="text-generation")
model = ChatHuggingFace(llm=llm)

class Review(BaseModel):
    key_themes: list[str] = Field(description="Write down all the key themes discussed in the review in a list")
    summary: str =Field(description="A brief summary of the review")
    sentiment_with_literal: Literal["pos", "neg"] = Field(description="Returns sentiment of the review either positive , negative or neutral")
    pros: Optional[list[str]] = Field(default=None, description= "write down all the pros inside a list")
    cons: Optional[list[str]] = Field(default=None, description= "write down all the cons inside a list")

class Person(BaseModel):
    name : str #= Field(description="Name of the person")
    age : int #= Field(description="Age of the person")
    city: str #= Field(description="City of the person where he belongs to")

#structured_model = model.with_structured_output(Review)
review1 = "The Realme P1 Speed is a good device for the money. It is now equipped with an enticing OLED panel, 120Hz refresh rate support and performance through MediaTek Dimensity 7300 SoC. It has a large 5000mAh battery and supports 45W charging, so it fits power users."

parser = PydanticOutputParser(pydantic_object=Person)
template = PromptTemplate(
    template = "Generate name, age and city of a fictional person from {place} \n {format_instruction}",
    input_variables=['place'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

chain = template | model | parser

#review1 = "The Realme P1 Speed is a good device for the money. It is now equipped with an enticing OLED panel, 120Hz refresh rate support and performance through MediaTek Dimensity 7300 SoC. It has a large 5000mAh battery and supports 45W charging, so it fits power users."
result = chain.invoke({"place": "Sri Lanka"})
print(chain.get_graph().print_ascii())
print(result)