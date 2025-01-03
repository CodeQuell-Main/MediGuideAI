import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_KEY")

def is_medical_academics_question(user_message):
    classification_prompt = [
        {
            "role": "system",
            "content": (
                "You are an assistant that determines if a question is related to medical academics for students. "
                "Medical academics include topics like diseases, anatomy, physiology, medical research, and treatments. "
                "Answer only 'Yes' or 'No' with no additional text."
            ),
        },
        {"role": "user", "content": f"Is the following query related to medical academics? \n\nQuery: \"{user_message}\""},
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=classification_prompt,
        max_tokens=5,
        temperature=0
    )
    
    classification = response['choices'][0]['message']['content'].strip().lower()
    # print(f"DEBUG: Classification response: {classification}")  # Debugging log

    return classification == "yes"

def generate_response(user_message):
    moderation_response = openai.Moderation.create(
        input=user_message
    )

    if moderation_response["results"][0]["flagged"]:
        return "Sorry, your message contains inappropriate content and cannot be processed."

    if not is_medical_academics_question(user_message):
        return "Sorry, I can only provide answers related to medical students' academics. Please ask a relevant question."

    messages = [
        {"role": "system", "content": """You are a medical student assistant, and you can only answer questions related to medical academics, such as anatomy, diseases, treatments, and medical research."""},
        {"role": "user", "content": user_message}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=50
    )
    
    return response['choices'][0]['message']['content']
