import streamlit as st

import anthropic

# Get api key from secrets.toml file
api_key = st.secrets["ANTHROPIC_API_KEY"]

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
        "fields": ["Topic", "Grade Level"],
        "user_prompt_template": """
            You are tasked with creating an engaging science lab based on a chosen topic and standard. Your goal is to design a lab that encourages hands-on learning, critical thinking, and inquiry-based exploration.

            Please follow these guidelines:

            Choose a science topic or standard that you would like to base your lab on.
            Develop a lab procedure that is safe, clear, and easy to follow.
            Include a list of materials and equipment needed for the lab.
            Provide clear instructions for setting up the experiment, performing the procedure, and recording observations.
            Incorporate opportunities for students to make predictions, analyze data, and draw conclusions.
            Include a discussion or reflection section where students can share their findings and insights.
            Here is the science topic or standard and grade level you will be working with:

            Topic: {{Topic}}

            Grade Level: {{Grade Level}}

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
        "fields": ["Topic", "Grade Level"],
        "user_prompt_template": """
            You are tasked with creating a spiral review problem set for a given math standard or topic. A spiral review is a method of revisiting previously learned concepts throughout the year to reinforce learning and maintain retention.

            Please follow these guidelines:

            Choose a math standard or topic to focus on.
            Create a problem set consisting of 10-15 problems that cover a variety of skills and concepts within the chosen standard or topic.
            Ensure that the problems are arranged in a way that progressively increases in difficulty.
            Include problems from different domains of mathematics, such as algebra, geometry, statistics, and probability, as applicable to the chosen standard or topic.
            Provide clear and concise instructions for each problem, and include an answer key at the end of the problem set.
            Here is the math standard or topic and grade level you will be working with:

            Topic: {{Topic}}

            Grade Level: {{Grade Level}}

            Please generate the spiral review problem set based on the given standard or topic.
        """,
    },
    "Group Work Generator": {
        "description": "Generate group work activity for students based on a a topic, standard, or objective.",
        "fields": ["Subject", "Topic"],
        "user_prompt_template": """
            You are tasked with creating a group work activity for students based on a given topic, standard, or objective. The goal of the activity is to promote collaboration, communication, and critical thinking among students.

            Please follow these guidelines:

            Choose a topic, standard, or objective that you would like to base your group work activity on.
            Determine the number of students per group and the roles they will play (e.g.g., leader, recorder, presenter).
            Develop a group work activity that is engaging, challenging, and relevant to the chosen topic, standard, or objective.
            Provide clear instructions for each group role and the overall group work process.
            Include a rubric or evaluation criteria for assessing group work performance.
            Here is the subject and topic, standard, or objective you will be working with:

            SUbject: {{Subject}}

            Topic: {{Topic}}

            Please generate a group work activity based on the given topic, standard, or objective.
        """,
    },
    "Make It Relevant": {
        "description": "Generate several ideas that make what you’re teaching relevant to your class based on their interests and background",
        "fields": ["Topic", "Student Interests"],
        "user_prompt_template": """
            You are tasked with generating several ideas that make the content you are teaching relevant to your students based on their interests and background. The goal is to create connections between the subject matter and your students' lives, making the learning experience more engaging and meaningful.

            Please follow these guidelines:

            Identify the topic, standard, or objective you will be teaching.
            Research your students' interests, hobbies, and backgrounds.
            Brainstorm several ideas that connect the subject matter to your students' lives, using their interests and backgrounds as a starting point.
            Develop activities, examples, or projects that incorporate these connections and make the content more relevant to your students.
            Consider using a variety of strategies, such as real-world examples, analogies, and personal stories, to engage your students and help them relate to the subject matter.
            Here is the topic, standard, or objective and student interests you will be working with:

            Topic: {{Topic}}

            Student Interests: {{Student Interests}}

            Please generate several ideas that make the given topic, standard, or objective relevant to your 
            class based on their interests and backgrounds.

        """,
    },
    "Write An Email": {
        "description": "Generate a draft of email for various uses such as administrative communication, parental communication or professional use about a certain subject with a choice of tone for the email",
        "fields": ["Subject", "Audience", "Tone", "Purpose"],
        "user_prompt_template": """
            You are tasked with generating a draft of an email for various uses, such as administrative 
            communication, parental communication, or professional use. The email should address a specific 
            subject and include the following components:

            Subject Line: Clearly state the main topic of the email in a concise and engaging manner.
            Introduction: Begin with a brief greeting and introduce the purpose of the email.
            Body: Provide relevant information and details about the subject, keeping the tone appropriate for 
            the intended audience.
            Conclusion: Summarize the main points and include a call to action or request, if applicable.
            Closing: End the email with a professional sign-off and your name or signature.
            Please provide the following information:

            Subject: {{Subject}}

            Audience: {{Audience}}

            Tone:{{Tone}}

            Purpose: {{Purpose}}

            Now, compose a draft of an email based on the provided information, keeping the tone and purpose in 
            mind. Make sure to address the subject clearly and professionally while engaging the intended 
            audience.
        """,
    },
    "Lesson Planner": {
        "description": "Generate a lesson plan for a topic or objective you’re teaching",
        "fields": ["Topic", "Grade Level", "Duration"],
        "user_prompt_template": """
            You are tasked with creating a lesson plan for a specific topic or objective that you will be teaching. Your lesson plan should include the following components:

            Objective: Clearly state the goal of the lesson and what students should be able to achieve by the end of the class.
            Materials: List all the materials and resources needed for the lesson, such as textbooks, handouts, and digital resources.
            Procedure: Provide a step-by-step outline of the lesson, including the time allocated for each activity and how you will engage students in the learning process.
            Assessment: Describe the methods you will use to assess students' understanding and progress during and after the lesson.
            Differentiation: Include strategies to accommodate diverse learning needs and abilities, such as providing visual aids, alternative activities, or additional support.
            Please provide the topic or objective you will be teaching, as well as the grade level and class duration:

            Topic: {{Topic}}

            Grade Level:{{Grade Level}}

            Class Duration: {{Duration}}
        """,
    },
    "Worksheet Generator": {
        "description": "Generate a worksheet based on any topic and grade level",
        "fields": ["Subject", "Topic", "Grade Level"],
        "user_prompt_template": """
            You are tasked with generating a worksheet based on a given topic and grade level. Your worksheet should include the following components:

            Introduction: Provide a brief overview of the topic and its relevance to the students' learning objectives.
            Tasks and Questions: Create a series of tasks and questions that are appropriate for the given grade level and aligned with the topic.
            Answer Key: Include an answer key or model solutions for the tasks and questions, as applicable.
            Please provide the following information:

            Subject: {{Subject}}

            Topic:{{Topic}}

            Grade Level: {{Grade Level}}
            Now, develop your worksheet using the guidelines provided above. Make sure to include one question for each DOK level to assess students' understanding at different depths of knowledge.

            DOK 1: Create a question that requires simple recall of facts, definitions, or basic concepts.
            DOK 2: Develop a question that involves skills, concepts, or mental processing beyond simple recall.
            DOK 3: Craft a question that demands strategic thinking, reasoning, and complex mental processing.
            DOK 4: Design a question that requires extended thinking, often over longer periods, and may involve real-world application or multiple concepts.
            Once you have created the worksheet, please provide the completed worksheet along with the answer key or model solutions.
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
task_to_process_function = {
    tool: lambda fields: process_tools(fields, tool) for tool in prompts_and_fields
}
