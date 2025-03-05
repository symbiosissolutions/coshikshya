from utils import generate_page, process_tools


# Define the app function to set up the Lesson Planner page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "📒",  # The icon to be displayed
        "Lesson Notes",  # The title of the page
        "Create engaging lesson notes that break down complex topics into clear, memorable points!",  # Description of the page's purpose
        [
            "Topic",
            "Grade Level",
            "Additional Materials",
        ],  # The fields needed for user input
        process_function=lambda fields: process_tools(
            fields, "Lesson Notes"
        ),  # Use the dynamic process function
        input_types={
            "Topic": "text_input",
            "Grade Level": "text_input",
            "Additional Materials": "file_upload",
        },
        placeholders={
            "Topic": "Pick any topic! Like: Forces and Motion, Trigonometry",
            "Grade Level": "Which grade is this for? (Grade 9, High School)",
        },
    )
