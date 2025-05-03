🏋️‍♂️ **Personal Fitness AI Coach**

An AI-powered personal fitness, nutrition, and health assistant that helps users track goals, manage personal data, and ask intelligent fitness-related questions — all connected to a robust database (Astra DB) and a Langflow-based AI pipeline!

📋 **Project Overview**

Personal Fitness AI Coach is a Streamlit web application that enables users to:

Maintain their personal profile (name, age, height, weight, gender, activity level)

Set and track fitness goals (muscle gain, fat loss, staying active)

Manage personal fitness notes

Get customized macro-nutrition suggestions

Ask an AI agent personalized health, fitness, and nutrition questions based on their profile and notes

The AI Agent is powered by a Langflow backend integrated with OpenAI's LLMs and AstraDB Vector Store retrieval for contextual awareness.

🚀 **Features**

📝 Profile Management: Store personal information securely in Astra DB

🎯 Goal Tracking: Select and update your fitness goals

🍎 Nutrition Macros Generator: Auto-generate calorie and macro recommendations with AI

📒 Notes Manager: Save important notes, reminders, and milestones

🤖 Ask AI: Personalized advice based on user's profile and stored notes

☁️ Serverless & Cloud Native: Integrates with Datastax Astra DB and Langflow APIs

🛠️ **Technology Stack**

Tech	Purpose
Python	Core development language
Streamlit	Front-end web interface
Astra DB	Cloud-native NoSQL database for storing user profiles and notes
Langflow	AI pipeline for processing queries
OpenAI Models	For generating intelligent and personalized responses
Requests	Handling API calls

🧩 **Folder Structure**


├── main.py              # Streamlit UI and workflow
├── ai.py                # AI agent integration (Langflow API call setup)
├── profiles.py          # Profile management functions
├── form_submit.py       # Form operations (add/update notes)
├── db.py                # Database connection and collections
├── .env                 # Environment variables (API keys, tokens)
├── README.md            # Project documentation (this file)


⚙️ **Setup Instructions**
Clone the repository:


git clone 
cd personal-fitness-ai-coach
Create and activate a virtual environment:


python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
Install required packages:


pip install -r requirements.txt
Setup Environment Variables:

Create a .env file:


ASTRA_DB_APPLICATION_TOKEN=<your-astra-db-token>
ASTRA_DB_API_ENDPOINT=<your-astra-db-endpoint>
ASK_AI_LANGFLOW_TOKEN=<your-langflow-api-token>
ASK_AI_FLOW_URL=<your-langflow-flow-url>
Run the application:


streamlit run main.py
Access the app at http://localhost:8501


🧠 **How It Works**

Step 1: User fills personal data (age, weight, height, etc.)

Step 2: User sets fitness goals and logs important notes

Step 3: User can generate nutrition macros or ask any fitness/nutrition question

Step 4: AI uses Langflow + AstraDB retrieval to give a contextual, personalized answer

✨ **Future Enhancements**

Fitness progress charts and history tracking 📈

Workout plan generator based on current goals 🏋️‍♀️

Advanced AI follow-up conversation memory 🧠

Meal planner and recipe generator 🥗

📬 **Contact If you like the project or want to collaborate, feel free to connect:**

GitHub: (https://github.com/KamalTeckchandani)

LinkedIn: https://www.linkedin.com/in/kamal-teckchandani/
