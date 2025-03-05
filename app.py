import streamlit as st
from streamlit_option_menu import option_menu

from views.lesson_planner import app as lesson_planner_app
from views.assessment_generator import app as assessment_generator_app
from views.lesson_notes import app as lesson_notes_app
from views.make_it_relevant import app as make_it_relevant_app
from views.write_an_email import app as write_an_email_app
from views.text_rewriter import app as text_rewriter_app


# Set up the page configuration with a title and an icon
st.set_page_config(
    page_title="CoShikshya",
    page_icon="👩‍🏫",
    layout="wide",
)


def main():
    # Create a sidebar with an option menu
    with st.sidebar:
        selected = option_menu(
            "CoShikshya",
            [
                "Lesson Planner",
                "Assessment Generator",
                "Lesson Notes",
                "Make It Relevant",
                "Text Rewriter",
                "Write An Email",
            ],
            icons=[
                "journal-plus",
                "clipboard2-check",
                "journals",
                "lightbulb",
                "vector-pen",
                "envelope-at",
            ],
            menu_icon=["book"],
            # Default selected item
            default_index=0,
            styles={
                "container": {"padding": "1rem", "background-color": "#f0f4f8"},
                "icon": {"color": "#00c6ff", "font-size": "1.4rem"},
                "nav-link": {
                    "font-size": "1rem",
                    "text-align": "left",
                    "margin": "0.5rem 0",
                    "border-radius": "0.5rem",
                    "background-color": "#ffffff",
                    "color": "#333333",
                    "--hover-color": "#e0e0e0",
                    "font-weight": "normal",
                },
                "nav-link-selected": {
                    "background-color": "#007bff",
                    "color": "#ffffff",
                    "font-weight": "600",
                },
            },
        )

    # Define a dictionary to map menu items to their corresponding functions
    menu_mapping = {
        "Lesson Planner": lesson_planner_app,
        "Assessment Generator": assessment_generator_app,
        "Lesson Notes": lesson_notes_app,
        "Make It Relevant": make_it_relevant_app,
        "Write An Email": write_an_email_app,
        "Text Rewriter": text_rewriter_app,
    }

    # Call the function based on the selected menu item
    if selected in menu_mapping:
        menu_mapping[selected]()


# Run the main function
if __name__ == "__main__":
    main()
