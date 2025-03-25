#from langchain_core.prompts import PromptTemplate
#from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM, pipeline
import os

#model_path = "F:/Python3/AA_Practice/genai/TinyLlama/hub/models--TinyLlama--TinyLlama-1.1B-Chat-v1.0/snapshots/fe8a4ea1ffedaf415f4da2f062534de366a451e6/config.json"
model_path = "F:/Python3/AA_Practice/genai/TinyLlama/hub/models--TinyLlama--TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path, load_in_8bit=True)

pipeline = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=100
)
llm = HuggingFacePipeline.from_model_id(pipeline=pipeline)
result = model.invoke("What is the capital of india")
print(result)

