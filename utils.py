import streamlit as st
from langchain.chat_models import AzureChatOpenAI
import os  
from dotenv import load_dotenv
from langchain_community.retrievers import BM25Retriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import AzureOpenAI  
from langchain_core.runnables import RunnableMap
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
# Environment Variables for Azure OpenAI

load_dotenv()

endpoint = os.getenv("ENDPOINT_URL")  
deployment = os.getenv("DEPLOYMENT_NAME")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")  

# Initialize Azure OpenAI Service client
client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-05-01-preview",
)

llm = AzureChatOpenAI(
    azure_endpoint=endpoint,  # Required
    api_key=subscription_key,  # Optional if using env variable
    deployment_name=deployment,  # Replace with your Azure deployment name
    model="gpt-4o-mini",  # Or "gpt-3.5-turbo" depending on your model
    api_version="2024-05-01-preview",
    temperature=0.7
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
                import PyPDF2
                from io import BytesIO

                uploaded_file = st.file_uploader(
                    field,
                    type=["doc", "docx", "pdf"],
                    key=f"{title.lower().replace(' ', '_')}_{field.lower()}",
                )

                if uploaded_file:
                    if uploaded_file.type == "application/pdf":
                        # Read PDF
                        pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
                        text = "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
                        inputs[field] = text

                    elif uploaded_file.type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
                        # Read DOCX using python-docx
                        from docx import Document
                        doc = Document(BytesIO(uploaded_file.read()))
                        text = "\n".join([para.text for para in doc.paragraphs])
                        inputs[field] = text

                    else:
                        st.error("Unsupported file format.")

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
def generate_response(task_description, user_prompt_template, fields, tool):
    # System prompt to guide the model's response
    system_prompt = f"{task_description}\n\n"

    if fields.get("Additional Materials"):
        retrieved_ans = documentRAG(fields.get("Additional Materials"))
        # st.write(retrieved_ans)
        if tool == "Assessment Generator":
            retrieved_ans = render_math_expressions(retrieved_ans)
            return st.markdown(f"### Assessment Generated: \n\n {retrieved_ans}")
        else:
            return retrieved_ans
        # system_prompt += retrieved_ans
    # Dynamically fill the user prompt template with the actual values from the fields
    user_prompt = user_prompt_template
    for key, value in fields.items():
        # print(key, value)
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
    response = completion.choices[0].message.content
    if tool == "Assessment Generator":
        response = render_math_expressions(response)
        return st.markdown(f"### Assessment Generated: \n\n {response}")
    else:
        return response


# Define the prompts and fields for different tasks
prompts_and_fields = {
    "Assessment Generator":{
        "description": "Generate customized assessments for students in markdown format.",
        "fields": ["Topic", "Grade Level", "Difficulty Level", "Number of Questions", "Additional Materials"],
        "user_prompt_template": """
                            You are an expert educator tasked with generating a well-structured assessment for students. The assessment should be based on the given topic, tailored to the specified grade level, and aligned with appropriate difficulty levels.

                            The assessment should include the following:

                            Objective: Clearly define what students should learn.
                            Question Types: Incorporate multiple-choice, short answer, and application-based questions.
                            Assessment Format: Structure the test logically, providing clear instructions.
                            Engagement: Ensure that the assessment promotes critical thinking and problem-solving.
                            Assessment Details:

                            Topic: {{Topic}}
                            Grade Level: {{Grade Level}}
                            Difficulty Level: {{Difficulty Level}}
                            Number of Questions: {{Number of Questions}}
                            """
    },
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
        task_info["description"], task_info["user_prompt_template"], fields, tool
    )


# Mapping task titles to the dynamic process function
task_to_process_function = {
    tool: lambda fields: process_tools(fields, tool) for tool in prompts_and_fields
}

import re

# Function to render LaTeX expressions with proper superscript formatting and other mathematical symbols
def render_math_expressions(text):
    # Replace LaTeX superscript with Unicode superscript
    superscript_dict = {
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵",
        "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "+": "⁺", "-": "⁻", "=": "⁼",
        "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ", "e": "ᵉ", "f": "ᶠ", "g": "ᵍ",
        "h": "ʰ", "i": "ⁱ", "j": "ʲ", "k": "ᵏ", "l": "ˡ", "m": "ᵐ", "n": "ⁿ",
        "o": "ᵒ", "p": "ᵖ", "q": "ᑫ", "r": "ʳ", "s": "ˢ", "t": "ᵗ", "u": "ᵘ",
        "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ", "z": "ᶻ"
    }

    # Handle superscripts in general
    def convert_superscript(match):
        base = match.group(1)
        exponent = match.group(2)
        converted_exponent = "".join([superscript_dict.get(char, char) for char in exponent])
        return base + converted_exponent

    # Handle LaTeX fractions like \frac{1}{2} --> "1/2"
    def convert_fraction(match):
        numerator = match.group(1)
        denominator = match.group(2)
        return f"{numerator}/{denominator}"

    # Handle integrals: \int_{1}^{4} --> ∫ from 1 to 4
    def convert_integral(match):
        lower_limit = match.group(1)
        upper_limit = match.group(2)
        return f"∫_{lower_limit}^{upper_limit}"

    # Handle logarithms: \ln --> ln
    def convert_log(match):
        return "ln"

    # Handle other functions like \tan^{-1} --> tan⁻¹
    def convert_inverse_function(match):
        function_name = match.group(1)
        return f"{function_name}⁻¹"

    # Apply regex replacements for various LaTeX math symbols
    text = re.sub(r"([a-zA-Z0-9])\^([a-zA-Z0-9]+)", convert_superscript, text)  # Superscript
    text = re.sub(r"\\frac\{([a-zA-Z0-9]+)\}\{([a-zA-Z0-9]+)\}", convert_fraction, text)  # Fraction
    text = re.sub(r"\\int\{([a-zA-Z0-9]+)\}\{([a-zA-Z0-9]+)\}", convert_integral, text)  # Integral
    text = re.sub(r"\\ln", convert_log, text)  # Logarithms
    text = re.sub(r"\\tan\^{-1}", convert_inverse_function, text)  # Inverse functions

    return text

# RAG Implementation

def documentRAG(doc):
    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_template("""
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, say that you don't know.
    Context: {context}
    Question: {question}
    """)
    splitter = RecursiveCharacterTextSplitter(chunk_size = 150, chunk_overlap = 10)
    chunks = splitter.split_text(doc)
    bm25_retriever = BM25Retriever.from_texts(chunks, k=3)
    # results = bm25_retriever.invoke("what would be lesson plan on listening skills?")
    chain = RunnableMap({
            "context": bm25_retriever, 
            "question": RunnablePassthrough()
        }) | prompt | llm | StrOutputParser()
    question = "What is a lesson plan for listening skills?"
    response = chain.invoke(question)
    # print(response)
    return response