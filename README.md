# HealthWise: Personalized Health Guide
A web application that generates personalized health reports and fitness advice by analyzing user-provided health data with the Google Gemini model.

## Live Application
The deployed application can be accessed here: https://healthwise.streamlit.app/

## Overview
HealthWise is an intelligent health and fitness guide designed to provide users with tailored wellness recommendations. By inputting basic demographic, lifestyle, and health history information, users can receive a comprehensive health report or ask specific questions related to diet, diseases, and fitness. The application leverages a powerful AI model to deliver safe, context-aware, and personalized advice.

##  Features
Personalized Health Profile: Collects key data points including age (calculated from date of birth), gender, BMI, activity level, and health goals.

Optional Health History: Allows users to securely provide sensitive information like pre-existing conditions and allergies for safer, more accurate recommendations.

Dual-Functionality Query System: Users can ask a specific health-related question or leave the query box blank to receive a general, holistic wellness report based on their profile.

Interactive UI: Built with Streamlit for a clean, intuitive, and responsive user experience.

## Technology Stack
Language: Python

Framework: Streamlit

AI Model: gemini-2.0 flash

Core Libraries: google-generativeai, pandas, python-dotenv

### Local Setup and Installation
To run this project on your local machine, please follow these steps.

#### Prerequisites
Python 3.8 or higher
A Google API Key with the Generative Language API enabled. You can obtain one from Google AI Studio.


1. Clone the Repository
git clone <your-repository-url>
cd <project-directory>

2. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
Create a requirements.txt file in the root of your project with the following content:

streamlit
pandas
google-generativeai
python-dotenv

Then, install the packages from the file:

pip install -r requirements.txt

4. Configure Environment Variables
Create a file named .env in the root directory of the project and add your Google API key to it.

GOOGLE_API_KEY='YOUR_API_KEY_HERE'

5. Run the Application
Launch the Streamlit application from your terminal.

streamlit run app.py

The application will now be running and accessible in your web browser, typically at http://localhost:8501.

## Usage
Navigate to the application URL.

Fill out the health profile fields within the "Enter Your Health Profile" section.

(Optional) To ask a specific question, type it into the text area.

(Optional) To receive a general report, leave the text area blank.

Click the "Generate Health Report" button.

The application will process your data and display a personalized report below the button.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
