import openai
from dotenv import load_dotenv
import os
import requests

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_KEY")

PUBMED_API_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

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
    return classification == "yes"

def fetch_pubmed_references(query, max_references=3):
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_references,
        "retmode": "json",
    }
    response = requests.get(f"{PUBMED_API_BASE}esearch.fcgi", params=params)
    
    if response.status_code != 200:
        return []
    
    article_ids = response.json().get("esearchresult", {}).get("idlist", [])
    references = []

    for article_id in article_ids:
        details_response = requests.get(
            f"{PUBMED_API_BASE}esummary.fcgi",
            params={
                "db": "pubmed",
                "id": article_id,
                "retmode": "json",
            }
        )
        if details_response.status_code == 200:
            details = details_response.json().get("result", {}).get(article_id, {})
            title = details.get("title", "No title available")
            link = f"https://pubmed.ncbi.nlm.nih.gov/{article_id}"
            references.append(f"{title} - [Read more]({link})")
    
    return references

def generate_response(user_message):
    moderation_response = openai.Moderation.create(
        input=user_message
    )

    if moderation_response["results"][0]["flagged"]:
        return "Sorry, your message contains inappropriate content and cannot be processed."

    if not is_medical_academics_question(user_message):
        return "Sorry, I can only provide answers related to medical students' academics. Please ask a relevant question."

    messages = [
        {"role": "system", "content": """You are a medical student assistant, and you can only answer questions related to medical academics, such as anatomy, diseases, treatments, and medical research. Keep your answers concise and ensure they fit within 80 tokens."""},
        {"role": "user", "content": user_message}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=80,
        temperature=0.7,
        stop=["\n", "."],
    )
    
    answer = response['choices'][0]['message']['content'].strip()
    
    references = fetch_pubmed_references(user_message)
    if references:
        answer += "\n\n**References:**\n" + "\n".join(references)
    
    return answer
