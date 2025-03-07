from utils import generate_page, process_tools


# Define the app function to set up the Lesson Planner page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "📝",  # The icon to be displayed
        "Lesson Planner",  # The title of the page
        "Generate a lesson plan for a topic or objective you’re teaching!",  # Description of the page's purpose
        [
            "Topic",
            "Grade Level",
            "Duration",
            "Subject",
            "Additional Materials",
        ],  # The fields needed for user input
        process_function=lambda fields: process_tools(
            fields, "Lesson Planner"
        ),  # Use the dynamic process function
        input_types={
            "Topic": "text_input",
            "Grade Level": "text_input",
            "Duration": "text_input",
            "Subject": "text_input",
            "Additional Materials": "file_upload",
        },
        placeholders={
            "Topic": "Pick any topic! Like: Photosynthesis, Fractions, World War II",
            "Grade Level": "Tell us the grade you're teaching: Grade 5, Middle School",
            "Duration": "How long is your class? (30 mins, 45 mins, 1 hour)",
        },
    )
