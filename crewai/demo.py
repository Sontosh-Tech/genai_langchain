from crewai import Crew, Agent, Task, Process
from langchain_ollama import OllamaLLM
# langchain.llms import Ollama
import os

#os.environ["OLLAMA_MODEL"] = "llama3.2"
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

#os.environ["OPENAI_API_KEY"] = "ollama"
#os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"

ollm = OllamaLLM(
    model="llama3.2",
    temperature=0.1,
    base_url="http://localhost:11434"
)


def create_agent(query):
    code_agent = Agent(
        role="Expert python developer",
        goal=f"Generate a python code to solve the problem : {query} and save the code in python file",
        backstory="You have more than 20 years of experience in python development",
        llm=ollm,
        allow_delegation=False
    )

    code_task = Task(
        description=f"Generate a python code to solve the problem : {query} and save the code in python file",
        expected_output=f"A production grade python code for the problem: {query} and save the code in python file",
        agent=code_agent,
        output_file="./generated_code/1.py"
    )

    crew = Crew(
        agents=[code_agent],
        tasks=[code_task],
        verbose=True,
        planning=True,
        planning_llm=ollm,  # MUST set this for planning
        #memory=False,            # MUST be False, or set a local embedder
        #embedder={
        #    "provider": "ollama",
        #    "config": {
        #        "model": "llama3.2",
        #        "base_url": "http://localhost:11434"
        #    }
        #}
    )

    return crew

def run_crew(query):
    crew = create_agent(query)
    result = crew.kickoff()
    print(result)

if __name__ == "__main__":
    query = "check if a number is armstrong"
    run_crew(query)
