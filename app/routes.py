from flask import Blueprint, request, jsonify
from .chatbot import generate_response

chatbot_routes = Blueprint("chatbot_routes", __name__)

@chatbot_routes.route("/ask", methods=["POST"])
def ask_bot():

    data = request.get_json()
    question = data.get("question")


    if not question:
        return jsonify({"error": "Question is required"}), 400
    
    # Generate the model's response
    answer = generate_response(question)

    # Return response as JSON
    return jsonify({"answer": answer})