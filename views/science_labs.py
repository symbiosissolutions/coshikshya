import streamlit as st
from utils import generate_page, process_science_labs

# Define the app function to set up the Science Labs page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "🧪",  # The icon to be displayed
        "Science Labs", # The title of the page
        "Generate an engaging science lab based on topics and standards of your choice!",  # Description of the page's purpose
        ["Topic"], # The fields needed for user input
        process_function=process_science_labs  # The function to process the inputs and generate the response
    )
