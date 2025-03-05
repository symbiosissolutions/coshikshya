from utils import generate_page, process_tools


# Define the app function to set up the Write An Email page
def app():
    # Call the generate_page function to create the page
    generate_page(
        "✍",  # The icon to be displayed
        "Text Rewriter",  # The title of the page
        "Simply upload your text or file, select the length, and get a rephrased version!",  # Description of the page's purpose
        [
            "Original Text",
            "Upload Text File",
            "Length Preference",
        ],  # The fields needed for user input
        process_function=lambda fields: process_tools(
            fields, "Text Rewriter"
        ),  # Use the dynamic process function
        input_types={
            "Original Text": "text_area",
            "Upload Text File": "file_upload",
            "Length Preference": "text_input",
        },
        placeholders={
            "Original Text": "Enter your text here... \nE.g. The quick brown fox jumps over the lazy dog.",
            "Length Preference": "E.g. shorter, similar, or longer",
        },
    )
