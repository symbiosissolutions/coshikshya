from utils import generate_page, process_tools


# Define the app function to set up the Group Work Generator page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "📋",  # The icon to be displayed
        "Group Work",  # The title of the page
        "Generate group work activity for students based on a a topic, standard, or objective!",  # Description of the page's purpose
        ["Subject", "Topic"],  # The fields needed for user input
        process_function=lambda fields: process_tools(
            fields, "Group Work Generator"
        ),  # Use the dynamic process function
    )
