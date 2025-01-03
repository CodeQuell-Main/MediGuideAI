from flask import Blueprint, request, jsonify, redirect, url_for, session, render_template, current_app
from flask_dance.contrib.google import google
from .chatbot import generate_response

chatbot_routes = Blueprint("chatbot_routes", __name__, template_folder="./templates", static_folder='static', static_url_path='./static')

@chatbot_routes.route("/")
@chatbot_routes.route("/login")
def login():
    if 'user' in session:
        return redirect(url_for('chatbot_routes.dashboard'))
    return render_template("login.html")

@chatbot_routes.route("/login/start")
def login_start():
    if google.authorized:
        return redirect(url_for('chatbot_routes.dashboard'))
    # print(f"Redirecting to: {url_for('google.login', _external=True)}")
    return redirect(url_for('google.login'))

@chatbot_routes.route("/login/callback")
def callback():
    if google.authorized:
        try:
            # print(f"Authorization code: {request.args.get('code')}")
            user_info = google.get('/oauth2/v2/userinfo').json()
            session['user'] = {
                "name": user_info['name'],
                "email": user_info['email'],
                "picture": user_info.get('picture')
            }
            return redirect(url_for('chatbot_routes.dashboard'))
        except Exception as e:
            return f"Failed to fetch user information: {str(e)}", 400
    return "Google OAuth failed", 400

@chatbot_routes.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect(url_for('chatbot_routes.login'))

    user = session['user']
    return render_template("dashboard.html", user=user)

@chatbot_routes.route("/ask", methods=["POST"])
def ask_bot():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized. Please log in first."}), 401

    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    answer = generate_response(question)

    return jsonify({"answer": answer})

@chatbot_routes.route("/logout")
def logout():
    session.pop('user', None)
    if google.authorized:
        google.get('/oauth2/v1/revoke?token=' + google.token['access_token'])
    session.clear()
    return redirect(url_for('chatbot_routes.login'))