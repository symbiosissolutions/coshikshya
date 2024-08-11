from utils import generate_page, process_tools


# Define the app function to set up the Make It Relevant page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "💡",  # The icon to be displayed
        "Make It Relevant",  # The title of the page
        "Generate several ideas that make what you’re teaching relevant to your class based on their interests and background!",  # Description of the page's purpose
        ["Topic"],  # The fields needed for user input
        process_function=lambda fields: process_tools(
            fields, "Make It Relevant"
        ),  # Use the dynamic process function
    )
