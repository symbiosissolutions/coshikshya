import streamlit as st
from utils import generate_page, process_dok_questions


# Define the app function to set up the DOK Questions page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "🙋‍♀️",  # The icon to be displayed
        "DOK Questions",  # The title of the page
        "Generate questions based on topic or standard for each of the 4 Depth of Knowledge (DOK) levels!",  # Description of the page's purpose
        ["Topic", "Grade Level"],  # The fields needed for user input
        process_function=process_dok_questions,  # The function to process the inputs and generate the response
    )
