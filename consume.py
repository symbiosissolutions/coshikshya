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

# Function to generate a lesson plan
def generate_lesson_plan(grade_level, subject, topic, duration):
    chat_prompt = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are an expert teacher and instructional designer skilled in using inquiry-focused teaching methods to effectively engage and challenge students through applied learning."
                }
            ]
        },
        {
            "role": "user",
            "content": f"""
                My grade {grade_level} students are studying {subject}. Your task is to design a lesson plan for this topic, based on the 5E instructional model, which has students Engage, Explore, Explain, Elaborate, and Evaluate. The lesson plan should be {duration} minutes long and should focus on {topic}. 
                
                The lesson plan should be aligned for grade {grade_level} and should include:
                - A list of key vocabulary
                - A lesson outline that includes a closure with a synthesis/summary of student learning
                - Options for differentiation
                - An assessment of learning
                
                **Step 1: Identify Objectives:**
                - Define Learning Objectives: Clearly outline what students should know, understand, or be able to do by the end of the lesson. Ensure these objectives are specific and measurable.
                - Align with Standards: Make sure your objectives align with educational standards or curriculum requirements.
                
                **Step 2: Engage:**
                - Capture Attention: Use open-ended questions, surprising demonstrations, or multimedia to spark curiosity and connect the topic to students’ prior knowledge.
                - Examples: Pose an intriguing question related to the topic, show a short, engaging video or animation, or introduce a hands-on activity that relates to the lesson content.
                
                **Step 3: Explore:**
                - Hands-On Activities: Design experiments or activities that allow students to investigate and discover concepts independently.
                - Encourage Inquiry: Allow students to ask questions and seek answers through their own exploration.
                - Examples: Conduct simple experiments related to the topic, provide materials for students to build models, or conduct investigations.
                
                **Step 4: Explain:**
                - Clarify Concepts: Prepare explanations that directly connect to students’ observations from the Explore phase. Use visual aids, discussions, or multimedia to clarify concepts.
                - Link to Real-World Applications: Explain how the concepts apply to real-world situations.
                - Examples: Use diagrams or videos to illustrate complex concepts, facilitate class discussions to clarify misunderstandings.
                
                **Step 5: Elaborate:**
                - Apply Knowledge: Design tasks that require students to apply their understanding in new or creative ways. This could involve problem-solving, critical thinking, or cross-disciplinary connections.
                - Examples: Challenge students to design a solution to a real-world problem, have students create models or presentations that apply the concept to different contexts.
                
                **Step 6: Evaluate:**
                - Assess Understanding: Use a mix of formative and summative assessments to measure students’ learning and provide feedback.
                - Examples: Administer quizzes or tests, have students present projects or reflect on their learning experience.
            """
        }
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

# Example usage
if __name__ == "__main__":
    grade_level = "7"  # Example Grade Level
    subject = "Science"  # Example Subject
    topic = "Photosynthesis"  # Example Topic
    duration = "45"  # Lesson duration in minutes

    lesson_plan = generate_lesson_plan(grade_level, subject, topic, duration)
    print(lesson_plan)
