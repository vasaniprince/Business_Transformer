from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from src.businessTransformer.tools.tools import research_tool, scrapper_tools, github_datasets_tools, kaggle_datasets_tools#, google_datasets_tools

import streamlit as st
import json
import os

from typing import Union, List, Tuple, Dict

from langchain_core.agents import AgentFinish

from langchain_google_genai import ChatGoogleGenerativeAI
from transformers import pipeline
from langchain_groq import ChatGroq
from langchain_community.llms import Ollama
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

import os
# os.environ["HUGGINGFACE_TOKEN"]=os.getenv("HUGGINGFACE_TOKEN")

@CrewBase
class UseCasesGenCrew:
    """UseCaseGen crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def llm(self):
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            convert_system_message_to_human=True
            )
        
        # llm = pipeline(
        #     "text-generation",
        #     model="EleutherAI/gpt-neo-2.7B",
        #     token=os.getenv("HUGGINGFACE_TOKEN")
        # )
        
        # llm=ChatGroq(
        #     model="llama3-8b-8192",#llama3-8b-8192
        #     groq_api_key=os.getenv("GROQ_API_KEY")
        # )
        
        # # llm = Ollama(model="mistral")
        # llm = Ollama(
        #     model="tinyllama",  # or whichever model you installed
        #     base_url="http://localhost:11434",
        #     temperature=0.7,
        #     timeout=120,
        #     # Optional: Reduce context window to save memory
        #     # context_window=2048,
        # )
        return llm
    
    def step_callback(
        self,
        agent_output: Union[str, List[Tuple[Dict, str]], AgentFinish],
        agent_name,
        *args,
    ):
        with st.chat_message("AI"):
            # Try to parse the output if it is a JSON string
            if isinstance(agent_output, str):
                try:
                    agent_output = json.loads(agent_output)
                except json.JSONDecodeError:
                    pass

            if isinstance(agent_output, list) and all(
                isinstance(item, tuple) for item in agent_output
            ):

                for action, description in agent_output:
                    # Print attributes based on assumed structure
                    st.write(f"Agent Name: {agent_name}")
                    st.write(f"Tool used: {getattr(action, 'tool', 'Unknown')}")
                    st.write(f"Tool input: {getattr(action, 'tool_input', 'Unknown')}")
                    st.write(f"{getattr(action, 'log', 'Unknown')}")
                    with st.expander("Show observation"):
                        st.markdown(f"Observation\n\n{description}")

            # Check if the output is a dictionary as in the second case
            elif isinstance(agent_output, AgentFinish):
                st.write(f"Agent Name: {agent_name}")
                output = agent_output.return_values
                st.write(f"I finished my task:\n{output['output']}")

            # Handle unexpected formats
            else:
                st.write(type(agent_output))
                st.write(agent_output)
                
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=research_tool,
            verbose=True,
            llm=self.llm(),
            step_callback=lambda step: self.step_callback(step, "Research Agent"),
            allow_delegation=False,
            max_retry_limit=1
        )
        
    @agent
    def ai_usecase_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["ai_usecase_agent"],
            verbose=True,
            tools=scrapper_tools,
            llm=self.llm(),
            step_callback=lambda step: self.step_callback(step, "Use Case Generator Agent"),
            allow_delegation=False,
            max_retry_limit=1
        )
    @agent
    def resource_collector(self) -> Agent:
        return Agent(
            config=self.agents_config["resource_collector"],
            verbose=True,
            tools=kaggle_datasets_tools+github_datasets_tools,
            allow_delegation=False,
            llm=self.llm(),
            step_callback=lambda step: self.step_callback(step, "Resource Collector Agent"),
            max_retry_limit=1
        )
        
    @task
    def industry_company_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["industry_company_research_task"],
            agent=self.researcher(),
            # output_file="industry_company_research.md",
        )
    
    @task
    def ai_usecase_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["ai_usecase_analysis_task"],
            agent=self.ai_usecase_agent(),
            # output_file="ai_usecase_analysis.md",
            dependencies=[self.industry_company_research_task()]
        )
        
    @task
    def resource_collection_task(self) -> Task:
        return Task(
            config=self.tasks_config["resource_collection_task"],
            agent=self.resource_collector(),
            # output_file="",
            dependencies=[self.ai_usecase_analysis_task()]            
        )

    @crew
    def crew(self) -> Crew:
        """Creates the UseCaseGen crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
        )