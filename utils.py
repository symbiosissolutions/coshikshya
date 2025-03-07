import streamlit as st
import os  
from openai import AzureOpenAI  
# Environment Variables for Azure OpenAI
endpoint = os.getenv("ENDPOINT_URL")  
deployment = os.getenv("DEPLOYMENT_NAME")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")  

# Initialize Azure OpenAI Service client
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",
)


# Generates a page in the Streamlit app with a form to collect user inputs.
def generate_page(
    icon,
    title,
    description,
    fields,
    process_function,
    input_types=None,
    placeholders=None,
):
    # Combine icon and title for the page header
    st.title(f"{icon} {title}")
    st.subheader(description)

    # Form to collect user inputs with unique key
    with st.form(f"{title.lower().replace(' ', '_')}_form"):
        inputs = {}
        input_types = input_types or {}
        placeholders = placeholders or {}

        for field in fields:
            field_type = input_types.get(field, "text_input")
            placeholder = placeholders.get(field, f"Enter {field.lower()} here...")

            if field_type == "text_area":
                inputs[field] = st.text_area(
                    field,
                    placeholder=placeholder,
                    height=200,
                    key=f"{title.lower().replace(' ', '_')}_{field.lower()}",
                )
            elif field_type == "file_upload":
                uploaded_file = st.file_uploader(
                    field,
                    type=["doc", "docx", "pdf"],
                    key=f"{title.lower().replace(' ', '_')}_{field.lower()}",
                )
                if uploaded_file:
                    inputs[field] = uploaded_file.read().decode()
            else:
                # Dictionary -> fields : st.text_input
                # eg "Topic": st.text_input("Topic", key="math_spiral_review_topic"
                inputs[field] = st.text_input(
                    field,
                    placeholder=placeholder,
                    key=f"{title.lower().replace(' ', '_')}_{field.lower()}",
                )

        submit = st.form_submit_button(label=f"Generate {title}")

        if submit:
            if process_function:
                if all(inputs.values()):
                    with st.spinner("Generating response..."):
                        response = process_function(inputs)
                    st.success(response)
                else:
                    st.error("Please fill out all fields.")
            else:
                st.error("Process function is not defined.")


# Generates a response based on the provided task description and fields.
def generate_response(task_description, user_prompt_template, fields):
    # System prompt to guide the model's response
    system_prompt = f"{task_description}\n\n"

    # Dynamically fill the user prompt template with the actual values from the fields
    user_prompt = user_prompt_template
    for key, value in fields.items():
        placeholder = f"{{{{{key}}}}}"
        if placeholder in user_prompt:
            user_prompt = user_prompt.replace(placeholder, value)


    chat_prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Generate the lesson plan using OpenAI
    completion = client.chat.completions.create(
        model=deployment,
        messages=chat_prompt,
        max_tokens=1000,  
        temperature=0.7,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,
        stop=None,  
        stream=False
    )

    return completion.choices[0].message.content


# Define the prompts and fields for different tasks
prompts_and_fields = {
    "Lesson Planner": {
        "description": "You are an expert teacher and instructional designer skilled in using inquiry-focused teaching methods to effectively engage and challenge students through applied learning.",
        "fields": ["Topic", "Grade Level", "Duration", "Subject"],
        "user_prompt_template": """
            My grade {{Grade Level}} students are studying the subject {{Subject}}. Your task is to design a lesson plan for this topic, based on the 5E instructional model, which has students Engage, Explore, Explain, Elaborate, and Evaluate. The lesson plan should be {{Duration}} minutes long and should focus on {{Topic}}. The lesson plan should be aligned for grade {{Grade Level}} and should include: a list of key vocabulary; a lesson outline that includes a closure with a synthesis/summary of student learning; options for differentiation; and an assessment of learning.

            Step 1: Identify Objectives:
            Define Learning Objectives: Clearly outline what students should know, understand, or be able to do by the end of the lesson. Ensure these objectives are specific and measurable.

            Align with Standards: Make sure your objectives align with educational standards or curriculum requirements.

            Step 2: Engage:
            Capture Attention: Use open-ended questions, surprising demonstrations, or multimedia to spark curiosity and connect the topic to students’ prior knowledge.

            Examples:
            Pose an intriguing question related to the topic.
            Show a short, engaging video or animation.
            Introduce a hands-on activity that relates to the lesson content.

            Step 3: Explore:
            Hands-On Activities: Design experiments or activities that allow students to investigate and discover concepts independently. Ensure materials and instructions are clear but not overly directive.

            Encourage Inquiry: Allow students to ask questions and seek answers through their own exploration.

            Examples:
            Conduct simple experiments related to the topic.
            Provide materials for students to build models or conduct investigations.
            Step 4: Explain:
            Clarify Concepts: Prepare explanations that directly connect to students’ observations from the Explore phase. Use visual aids, discussions, or multimedia to clarify concepts.

            Link to Real-World Applications: Explain how the concepts apply to real-world situations.

            Examples:
            Use diagrams or videos to illustrate complex concepts.
            Facilitate class discussions to clarify misunderstandings.

            Step 5: Elaborate:
            Apply Knowledge: Design tasks that require students to apply their understanding in new or creative ways. This could involve problem-solving, critical thinking, or cross-disciplinary connections.

            Examples:
            Challenge students to design a solution to a real-world problem related to the topic.
            Have students create models or presentations that apply the concept to different contexts.

            Step 6: Evaluate:
            Assess Understanding: Use a mix of formative and summative assessments to measure students’ learning and provide feedback.

            Examples:
            Administer quizzes or tests.
            Have students present projects or reflect on their learning experience.

            Please generate the lesson plan according to the guidelines above.
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
