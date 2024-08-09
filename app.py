import streamlit as st
from streamlit_option_menu import option_menu

from views.science_labs import app as science_labs_app
from views.math_spiral_review import app as math_spiral_review_app  
from views.dok_questions import app as dok_questions_app


# Set up the page configuration with a title and an icon
st.set_page_config(
    page_title="CoShikshya",
    page_icon="👩‍🏫",
)

def main():
    # Create a sidebar with an option menu
    with st.sidebar:
        selected = option_menu(
            "CoShikshya",
            ["DOK Questions", "Math Spiral Review", "Science Labs"],
            icons=["journals", "calculator", "funnel"],
            menu_icon = ["book"],
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

    # Conditional rendering based on the selected menu item
    if selected == "Science Labs":
        science_labs_app()
    elif selected == "Math Spiral Review":
        math_spiral_review_app()
    elif selected == "DOK Questions":
        dok_questions_app()

# Run the main function
if __name__ == "__main__":
    main()
