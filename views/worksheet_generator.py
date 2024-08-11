from utils import generate_page, process_tools


# Define the app function to set up the Worksheet Generator page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "📋",  # The icon to be displayed
        "Worksheet",  # The title of the page
        "Generate a worksheet based on any topic and grade level!",  # Description of the page's purpose
        ["Topic", "Grade Level"],  # The fields needed for user input
        process_function=lambda fields: process_tools(
            fields, "Worksheet Generator"
        ),  # Use the dynamic process function
    )
