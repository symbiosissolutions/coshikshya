from utils import generate_page, process_tools


# Define the app function to set up the Lesson Planner page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "📝",  # The icon to be displayed
        "Assessment Generator",  # The title of the page
        "Generate customized assessments by selecting the topic, grade level, difficulty, and source material. Choose the number of questions to create a tailored assessment!",  # Description of the page's purpose
        [
            "Topic",
            "Grade Level",
            "Difficulty Level",
            "Number of Questions",
            "Additional Materials",
        ],  # The fields needed for user input
        process_function=lambda fields: process_tools(
            fields, "Assessment Generator"
        ),  # Use the dynamic process function
        input_types={
            "Topic": "text_input",
            "Grade Level": "text_input",
            "Difficulty Level": "text_input",
            "Number of Questions": "text_input",
            "Additional Materials": "file_upload",
        },
        placeholders={
            "Topic": "Pick any topic! Like: Solar System, Decimals, Parts of Speech",
            "Grade Level": "Tell us the grade you're teaching: Grade 7, High School",
            "Difficulty Level": "How tough should it be? (Easy, Medium, or Hard)",
            "Number of Questions": "How many? Like: 5 for a quick quiz, 10 for homework, 20 for chapter test",
        },
    )
