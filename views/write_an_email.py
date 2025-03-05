from utils import generate_page, process_tools


# Define the app function to set up the Write An Email page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "📧",  # The icon to be displayed
        "Write An Email",  # The title of the page
        "Generate an email draft for different purposes like school updates, parent communication, or work emails. Choose the tone that fits your message!",  # Description of the page's purpose
        [
            "Subject",
            "Audience",
            "Tone",
            "Key Details",
        ],  # The fields needed for user input
        process_function=lambda fields: process_tools(
            fields, "Write An Email"
        ),  # Use the dynamic process function
        placeholders={
            "Subject": "E.g. Parent-Teacher Conference Schedule",
            "Audience": "E.g. Parents, School Board, Students",
            "Tone": "E.g. Professional, Friendly, Formal",
            "Key Details": "E.g. Meeting on Tuesday at 3 PM in Room 204",
        },
    )
