# MediGuide AI

MediGuide AI is a study assistant designed specifically for medical students. It includes a chatbot feature that allows students to interact with the bot to get answers to their academic questions and clarify complex medical concepts. The chatbot is powered by AI, making it capable of providing accurate, reliable responses to a wide range of academic inquiries.

## Features

- **AI-Powered Chatbot**: The chatbot helps medical students by providing answers to academic problems, explaining medical terms, and clarifying concepts based on user queries.
- **Medical Term Explanations**: The bot offers detailed and understandable explanations of complex medical terminology to help students better grasp their studies.
- **Google Authentication**: Secure login using Google accounts for easy access to the platform.
- **User-Friendly Interface**: The platform is designed to be intuitive, ensuring a smooth experience for students as they interact with the chatbot.

## Installation

### Prerequisites

Ensure you have the following installed on your machine:

- Python 3.6+
- Node.js (for front-end if applicable)

### Clone the repository

```bash
git clone https://github.com/CodeQuell-Main/MediGuideAI.git
cd medi-guide-ai
```

### Setting up the Backend

1. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install the required packages**

```bash
pip install -r requirements.txt
```

3. **Set up Google OAuth 2.0**

   - Go to the [Google Developer Console](https://console.developers.google.com/).
   - Create a new project or select an existing one.
   - Navigate to **Credentials** and click **Create Credentials**.
   - Select **OAuth 2.0 Client IDs** and configure it for your app. Add the correct redirect URI and save the generated credentials.
   - Add these credentials to your project as environment variables or in a configuration file.

4. **Start the backend server**

```bash
python run.py
```

## Usage

Once everything is set up:

1. Open your browser and navigate to `http://localhost:5000` (or the appropriate port).
2. Sign in using the "Login with Google" button.
3. Start interacting with the chatbot to get answers to your academic questions or clarifications on medical concepts.

## Google Authentication Setup

For secure login, the project uses Google OAuth 2.0. Ensure that you’ve set up the OAuth credentials in the Google Developer Console as mentioned above. The system will handle user authentication and redirect the user accordingly.

## Contributing

Feel free to fork this repository, make changes, and submit a pull request. Contributions to improve the chatbot functionality or add new features are highly welcome!

## License

This project is licensed under the Apache License 2.0. See the LICENSE file for more details. - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google OAuth 2.0 for authentication
- AI libraries used for chatbot development
- Open-source contributors and libraries
