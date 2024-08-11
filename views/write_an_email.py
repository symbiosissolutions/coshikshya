from utils import generate_page, process_tools


# Define the app function to set up the Write An Email page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "📧",  # The icon to be displayed
        "Email",  # The title of the page
        "Generate a draft of email for various uses such as administrative communication, parental communication or professional use about a certain subject with a choice of tone for the email!",  # Description of the page's purpose
        ["Subject", "Audience", "Tone", "Purpose"],  # The fields needed for user input
        process_function=lambda fields: process_tools(
            fields, "Write An Email"
        ),  # Use the dynamic process function
    )
