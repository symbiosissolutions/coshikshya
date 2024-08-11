from utils import generate_page, process_tools


# Define the app function to set up the Lesson Planner page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "📝",  # The icon to be displayed
        "Lesson Planner",  # The title of the page
        "Generate a lesson plan for a topic or objective you’re teaching!",  # Description of the page's purpose
        ["Topic", "Grade Level", "Duration"],  # The fields needed for user input
        process_function=lambda fields: process_tools(
            fields, "Lesson Planner"
        ),  # Use the dynamic process function
    )
