import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_KEY")

def is_medical_academics_question(user_message):
    classification_prompt = f"""
    Determine if the following query is related to medical students' academics.
    Respond with "Yes" if it is, otherwise respond with "No".
    
    Query: "{user_message}"
    """
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=classification_prompt,
        max_tokens=10,
        temperature=0
    )
    
    classification = response['choices'][0]['text'].strip()
    return classification.lower() == "yes"

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
        max_tokens=500
    )
    
    return response['choices'][0]['message']['content']
