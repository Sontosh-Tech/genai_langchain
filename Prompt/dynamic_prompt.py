from langchain_core.prompts import PromptTemplate, load_prompt
from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline
import os
import streamlit as st

os.environ["HF_HOME"] = "F:/Python3/AA_Practice/genai/TinyLlama"
llm = HuggingFacePipeline.from_model_id(model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0", task="text-generation")
model = ChatHuggingFace(llm=llm)

st.header("Dynamic Prompt with Langchain")
paper_input = st.selectbox("Select Paper Name", ["Select...", "Attention is all you need", "BERT: Pre-training if Deep Bidirectional Transformers"])
style_input = st.selectbox("Select Explanation Style", ["Beginner Friendly", "Technical", 'Code-Oriented',"Mathematical"])
length_input = st.selectbox("Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"])

template = load_prompt("template_researchPaper.json")

#template = PromptTemplate(
#    template="""
#    Please summarize the research paper titled "{paper_input}" with the following specifications:
#    Explanation Style: {style_input}
#    Explanation Length: {length_input}
#    1. Mathematical Details:
#        - Include relavant mathematical equations if present in the paper.
#        - Explain the mathematical concepts using simple, intuitive code snippets where applicable.
#    2. Analogies:
#        - Use relatable analogies to simplify complex ideas.
#    If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.
#    Ensure the summary is clear, accurate and aligned with the provided style and length.
#    """,
#    input_variables=['paper_input', 'style_input', 'length_input'],
#    validate_template=True # default template validation
#)

#fill the placeholder
prompt = template.invoke({
    'paper_input':paper_input,
    'style_input':style_input,
    'length_input':length_input
})

if st.button("Summarize"):
    result = model.invoke(prompt)
    st.write(result.content)


