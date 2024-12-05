from src.businessTransformer.crew import UseCasesGenCrew

# def load_html_template(): 
#     with open('src/newsletter_gen/config/newsletter_template.html', 'r') as file:
#         html_template = file.read()
        
#     return html_template


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'company': input('Enter the company for use cases and resources: '),
    }
    UseCasesGenCrew().crew().kickoff(inputs=inputs)