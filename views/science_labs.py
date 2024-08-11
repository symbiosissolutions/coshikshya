from utils import generate_page, process_tools

# Define the app function to set up the Science Labs page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "🧪",  # The icon to be displayed
        "Science Labs", # The title of the page
        "Generate an engaging science lab based on topics and standards of your choice!",  # Description of the page's purpose
        ["Topic"], # The fields needed for user input
        process_function=lambda fields: process_tools(fields, "Science Labs")  # Use the dynamic process function
    )