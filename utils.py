import streamlit as st

# import os
# from dotenv import load_dotenv

# from langchain_anthropic import ChatAnthropic
import anthropic

# Get api key from secrets.toml file
api_key = st.secrets.api.ANTHROPIC_API_KEY

# model = ChatAnthropic(model='claude-3-opus-20240229')
client = anthropic.Anthropic()


# Generates a page in the Streamlit app with a form to collect user inputs.
def generate_page(icon, title, description, fields, process_function):
    # Combine icon and title for the page header
    st.title(f"{icon} {title}")
    st.subheader(description)

    # Form to collect user inputs with unique key
    with st.form(f"{title.lower().replace(' ', '_')}_form"):
        inputs = {}
        for field in fields:
            # Dictionary -> fields : st.text_input
            # eg "Topic": st.text_input("Topic", key="math_spiral_review_topic"
            inputs[field] = st.text_input(
                field, key=f"{title.lower().replace(' ', '_')}_{field.lower()}"
            )

        submit = st.form_submit_button(label=f"Generate {title}")

        if submit:
            if all(inputs.values()):
                with st.spinner("Generating response..."):
                    response = process_function(inputs)
                st.success(response)
            else:
                st.error("Please fill out all fields.")


# Generates a response based on the provided task description and fields.
def generate_response(task_description, user_prompt_template, fields):
    # System prompt to guide the model's response
    system_prompt = f"You are an AI assistant helping {task_description}."

    # Dynamically fill the user prompt template with the actual values from the fields
    user_prompt = user_prompt_template
    for key, value in fields.items():
        user_prompt = user_prompt.replace(f"{{{{{key}}}}}", value)

    # Create a message using the Claude model to generate the response
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system=system_prompt,
        messages=[{"role": "user", "content": [{"type": "text", "text": user_prompt}]}],
    )

    # Return the generated text from the message
    return message.content[0].text


# Define the prompts and fields for different tasks
prompts_and_fields = {
    "Science Labs": {
        "description": "Generate a detailed science lab activity.",
        "fields": ["Topic"],
        "user_prompt_template": """
           You are tasked with creating an engaging science lab based on a chosen topic and standard. 
           Your goal is to design a lab that encourages hands-on learning, critical thinking, and inquiry-based exploration.
            Please follow these guidelines:

            Choose a science topic or standard that you would like to base your lab on.
            Develop a lab procedure that is safe, clear, and easy to follow.
            Include a list of materials and equipment needed for the lab.
            Provide clear instructions for setting up the experiment, performing the procedure, and recording observations.
            Incorporate opportunities for students to make predictions, analyze data, and draw conclusions.
            Include a discussion or reflection section where students can share their findings and insights.
            Here is the science topic or standard you will be working with:

            Topic: {{Topic}}

            Please create an engaging science lab based on the given topic or standard.
        """,
    },
    "DOK Questions": {
        "description": "Generate Depth of Knowledge (DOK) questions for a given topic.",
        "fields": ["Topic", "Grade Level"],
        "user_prompt_template": """
            You are tasked with generating questions based on a given topic or standard for each of the 4 Depth of Knowledge (DOK) levels. The Depth of Knowledge levels represent the complexity and depth of understanding required to answer a question:

            - DOK 1: Recall and Reproduction
            - DOK 2: Skills and Concepts
            - DOK 3: Strategic Thinking
            - DOK 4: Extended Thinking

            Here is the topic or standard and grade level you will be working with:

            Topic: {{Topic}}

            Grade Level: {{Grade Level}}

            Your task is to generate one question for each DOK level based on this topic or standard. Follow these guidelines for each level:

            1. DOK 1: Create a question that requires simple recall of facts, definitions, or basic concepts.
            2. DOK 2: Develop a question that involves skills, concepts, or mental processing beyond simple recall.
            3. DOK 3: Craft a question that demands strategic thinking, reasoning, and complex mental processing.
            4. DOK 4: Design a question that requires extended thinking, often over longer periods, and may involve real-world application or multiple concepts
        """,
    },
    "Math Spiral Review": {
        "description": "Generate a spiral review problem set for a given math standard or topic.",
        "fields": ["Topic"],
        "user_prompt_template": """
            You are tasked with creating a spiral review problem set for a given math standard or topic. A spiral review is a method of revisiting previously learned concepts throughout the year to reinforce learning and maintain retention.

            Please follow these guidelines:

            Choose a math standard or topic to focus on.
            Create a problem set consisting of 10-15 problems that cover a variety of skills and concepts within the chosen standard or topic.
            Ensure that the problems are arranged in a way that progressively increases in difficulty.
            Include problems from different domains of mathematics, such as algebra, geometry, statistics, and probability, as applicable to the chosen standard or topic.
            Provide clear and concise instructions for each problem, and include an answer key at the end of the problem set.
            Here is the math standard or topic you will be working with:

            Topic: {{Topic}}

            Please generate the spiral review problem set based on the given standard or topic.
        """,
    },
    "Group Work Generator": {
        "description": "Generate group work activity for students based on a a topic, standard, or objective.",
        "fields": ["Topic"],
        "user_prompt_template": """
            You are tasked with creating a group work activity for students based on a given topic, standard,
            or objective. The goal of the activity is to promote collaboration, communication, and critical 
            thinking among students.

            Please follow these guidelines:

            Choose a topic, standard, or objective that you would like to base your group work activity on.
            Determine the number of students per group and the roles they will play (e.g.g., leader, recorder, presenter).
            Develop a group work activity that is engaging, challenging, and relevant to the chosen topic, standard, or objective.
            Provide clear instructions for each group role and the overall group work process.
            Include a rubric or evaluation criteria for assessing group work performance.
            Here is the topic, standard, or objective you will be working with:

            Topic: {{Topic}}

            Please generate a group work activity based on the given topic, standard, or objective.
        """,
    },
}


# Dynamic process function for all tools
def process_tools(fields, tool):
    task_info = prompts_and_fields[tool]
    return generate_response(
        task_info["description"], task_info["user_prompt_template"], fields
    )

# Mapping task titles to the dynamic process function
task_to_process_function = {tool: lambda fields: process_tools(fields, tool) for tool in prompts_and_fields}
