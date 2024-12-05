import streamlit as st
from src.businessTransformer.crew import UseCasesGenCrew

class UseCaseGenUI:
    
    # def load_markdown_template(self):
    #     with open("src/CreationScope/config/newsletter_template.html", "r") as file:
    #         markdown_template = file.read()

    #     return markdown_template
    
    def generate_use_cases(self,company):
        inputs = {
            "company": company,
            # "personal_message": personal_message,
            # "html_template": self.load_html_template(),
        }
        return UseCasesGenCrew().crew().kickoff(inputs=inputs)
    
    def use_case_generation(self):

        if st.session_state.generating:
            st.session_state.use_cases = self.generate_use_cases(
                st.session_state.company
            )

        if st.session_state.use_cases and st.session_state.use_cases != "":
            with st.container():
                st.write("Use Cases generated successfully!")
                st.download_button(
                    label="Download Report",
                    data=st.session_state.use_cases,
                    file_name="use_cases.md",
                    mime="text/markdown",
                )
            st.session_state.generating = False
    
    def sidebar(self):
        with st.sidebar:
            st.title("Use Case Generator")

            st.write(
                """
                To generate a newsletter, enter a company name and a groq api key. \n
                Your team of AI agents will generate a use case for that company!
                """
            )

            st.text_input("Company", key="company", placeholder="ABC Pvt Ltd.")
            
            if st.button("Generate Use Cases"):
                st.session_state.generating = True
    
    def render(self):
        st.set_page_config(page_title="Reports Generation", page_icon="📧",layout="wide")
        
        st.title("creation scope")

        if "company" not in st.session_state:
            st.session_state.topic = ""
            
        if "use_cases" not in st.session_state:
            st.session_state.use_cases=""

        if "generating" not in st.session_state:
            st.session_state.generating = False

        self.sidebar()

        self.use_case_generation()


if __name__ == "__main__":
    UseCaseGenUI().render()