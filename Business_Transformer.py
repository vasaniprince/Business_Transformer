import streamlit as st

st.set_page_config(page_title="BusinessTransformer",layout="wide")
st.title(":blue[BusinessTransformer]")


st.subheader("How it Works?", divider="rainbow")
st.write("""Our multi-agent AI system operates as your intelligent research assistant, powered by three specialized agents working in harmony. When you input a company name, the Research Agent first scours the internet to gather comprehensive information about the company's core business and strategic focus. This intelligence is then passed to our Use Case Generator Agent, which analyzes the data to identify promising opportunities for implementing AI technologies like GenAI, LLMs, and ML solutions within the company's context. Finally, our Resource Collector Agent steps in to locate relevant datasets, models, and implementation resources from platforms like Kaggle, HuggingFace, and GitHub, ensuring that each proposed AI solution has practical resources to support its implementation. The entire process culminates in a detailed report that bridges the gap between possibility and practicality in AI adoption.""")

st.header("What is the approach behind it?", divider="rainbow")
col1,col2,col3=st.columns([1,2,1])
with col2:
    st.image(r"E:\ai_planet\CreationScope-streamlit\assets\Project_Workflow.jpg")
st.write("Our approach leverages Crew AI's multi-agent architecture to create an intelligent system that breaks down complex AI implementation analysis into manageable, specialized tasks. Each agent in our system acts as an expert in its domain - from company research to use case generation and resource collection. Through this orchestrated workflow, the agents work in harmony: gathering comprehensive company information, analyzing AI implementation possibilities focusing on GenAI and LLMs, and matching these opportunities with practical resources from leading platforms. This systematic division of responsibilities ensures both efficiency and thoroughness in delivering actionable AI implementation strategies.")

st.markdown("---")
st.subheader("Let's Connect")
st.write("LinkedIn: https://www.linkedin.com/in/prince-vasani-634a35236/")
st.write("GitHub: https://github.com/vasaniprince")
st.write("Email: princeavasani@gmail.com")
st.write("Phone: +91 9016464656")