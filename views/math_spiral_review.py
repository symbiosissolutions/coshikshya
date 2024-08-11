from utils import generate_page, process_tools


# Define the app function to set up the Math Spiral Review page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "➗",  # The icon to be displayed
        "Math Spiral Review",  # The title of the page
        "Generate a spiral review problem set for any math standards or topics!",  # Description of the page's purpose
        ["Topic"],  # The fields needed for user input
        process_function=lambda fields: process_tools(
            fields, "Math Spiral Review"
        ),  # Use the dynamic process function
    )
