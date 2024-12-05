from crewai_tools import SerperDevTool, WebsiteSearchTool, SeleniumScrapingTool
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

research_tool = [SerperDevTool()]

scrapper_tools = [
    SerperDevTool(),
    WebsiteSearchTool(
        website="https://www.mckinsey.com/",
        config=dict(
            llm=dict(
                provider="google", 
                config=dict(
                    model="gemini-1.5-flash"
                ),
            ),
            embedder=dict(
                provider="google",
                config=dict(
                    model="models/embedding-001",
                    task_type="retrieval_document",
                ),
            ),
        ),
        max_retries=3,
        timeout=45  # increased timeout
    ),
    SeleniumScrapingTool(website_url="https://www.mckinsey.com/")
]

github_datasets_tools=[
    WebsiteSearchTool(
        website="https://github.com/search?q=datasets&type=repositories",
        config=dict(
            llm=dict(
                provider="google", 
                config=dict(
                    model="gemini-1.5-flash"
                ),
            ),
            embedder=dict(
                provider="google",
                config=dict(
                    model="models/embedding-001",
                    task_type="retrieval_document",
                ),
            ),
        )
    ),
    SeleniumScrapingTool(website_url="https://github.com/search?q=datasets&type=repositories")
]

kaggle_datasets_tools=[
    WebsiteSearchTool(
        website="https://www.kaggle.com/datasets",
        config=dict(
            llm=dict(
                provider="google", 
                config=dict(
                    model="gemini-1.5-flash"
                ),
            ),
            embedder=dict(
                provider="google",
                config=dict(
                    model="models/embedding-001",
                    task_type="retrieval_document",
                ),
            ),
        )
    ),
    SeleniumScrapingTool(website_url="https://www.kaggle.com/datasets")
]

# google_datasets_tools=[
#     WebsiteSearchTool(
#         website="https://datasetsearch.research.google.com/",
#         config=dict(
#             llm=dict(
#                 provider="google", 
#                 config=dict(
#                     model="gemini-1.5-flash"
#                 ),
#             ),
#             embedder=dict(
#                 provider="google",
#                 config=dict(
#                     model="models/embedding-001",
#                     task_type="retrieval_document",
#                 ),
#             ),
#         )
#     ),
#     SeleniumScrapingTool(website_url="https://datasetsearch.research.google.com/")
# ]