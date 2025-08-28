from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import google.generativeai as genai
import traceback

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the Gemini model
# It's good practice to wrap this in a try-except block in case of initialization errors
try:
    model = genai.GenerativeModel("gemini-pro")
except Exception as e:
    st.error(f"Error initializing the AI model: {e}")
    st.stop() # Stop the app if the model fails to initialize

# ---------------- Page Configuration ----------------
# This should be the first Streamlit command in your script
st.set_page_config(page_title="MyHealthify", layout="centered")

# ---------------- Sidebar Content ----------------
st.sidebar.header("Your Health Profile")
st.sidebar.markdown("Provide your details for a more personalized experience.")

# --- Basic Demographics ---
age = st.sidebar.number_input("Age:", min_value=1, max_value=120, step=1)
gender = st.sidebar.selectbox("Gender:", ["Male", "Female", "Other"])

# --- BMI Calculator ---
st.sidebar.subheader("⚖️ BMI Calculator")
weight = st.sidebar.text_input("Weight (kg):")
height = st.sidebar.text_input("Height (cm):")
bmi_value = None # Initialize BMI value

try:
    weight_num = pd.to_numeric(weight)
    height_num = pd.to_numeric(height)
    if weight_num > 0 and height_num > 0:
        bmi_value = weight_num / ((height_num / 100) ** 2)
        st.sidebar.markdown(f"**Your BMI is:** `{bmi_value:.2f}`")
    elif weight and height: # Show info only if both fields are touched
        st.sidebar.warning("Please enter valid positive numbers.")
except (ValueError, TypeError):
    if weight or height: # Show info only if user starts typing
        st.sidebar.info("Enter numerical values to calculate BMI.")

st.sidebar.markdown("""
**BMI Categories:**
- 🟦 Underweight: BMI < 18.5
- 🟩 Normal weight: 18.5 ≤ BMI < 25
- 🟨 Overweight: 25 ≤ BMI < 30
- 🟥 Obese: BMI ≥ 30
""")

# --- Lifestyle Information ---
st.sidebar.subheader("Lifestyle")
activity_level = st.sidebar.selectbox("Activity Level:", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
health_goal = st.sidebar.text_input("Primary Health Goal:", placeholder="e.g., Lose Weight, Gain Muscle")
diet_prefs = st.sidebar.text_input("Dietary Preferences:", placeholder="e.g., Vegetarian, Vegan, Gluten-Free")

# --- Health History (Optional) ---
st.sidebar.subheader("Health History (Optional)")
st.sidebar.info("Providing these details will result in a much safer and more personalized response.")
conditions = st.sidebar.text_area("Pre-existing Medical Conditions:", placeholder="e.g., Type 2 Diabetes, High Blood Pressure")
allergies = st.sidebar.text_area("Known Allergies:", placeholder="e.g., Peanuts, Shellfish")
sleep = st.sidebar.text_input("Average Sleep per Night:", placeholder="e.g., 7 hours")
habits = st.sidebar.selectbox("Smoking/Alcohol Habits:", ["None", "Occasionally", "Regularly"])


# ---------------- Main Content ----------------
st.header(":green[MyHealthify]–Your Health & Fitness Guide 💊", divider="red")

user_input = st.text_area("Ask me anything about Health, Diseases, or Fitness:", height=150)

# Gemini Response Function
def guide_me_on(query, user_profile):
    if not query.strip():
        return "⚠️ Please enter a health-related question."

    # Construct a detailed context string from the user's profile
    profile_context = (
        f"Here is the user's health profile:\n"
        f"- Age: {user_profile['age']}\n"
        f"- Gender: {user_profile['gender']}\n"
        f"- Weight: {user_profile['weight']} kg\n"
        f"- Height: {user_profile['height']} cm\n"
        f"- BMI: {user_profile['bmi']:.2f}\n"
        f"- Activity Level: {user_profile['activity_level']}\n"
        f"- Primary Health Goal: {user_profile['health_goal']}\n"
        f"- Dietary Preferences: {user_profile['diet_prefs']}\n"
    )

    # Add optional info only if provided
    if user_profile['conditions']:
        profile_context += f"- Pre-existing Conditions: {user_profile['conditions']}\n"
    if user_profile['allergies']:
        profile_context += f"- Allergies: {user_profile['allergies']}\n"
    if user_profile['sleep']:
        profile_context += f"- Sleep Habits: {user_profile['sleep']}\n"
    if user_profile['habits'] != "None":
        profile_context += f"- Smoking/Alcohol Habits: {user_profile['habits']}\n"

    system_prompt = (
        "You are a certified Dietician, Health Coach, and Fitness Expert. "
        "Your response must be based on the user's provided health profile. "
        "Respond to health, disease, and fitness-related questions with empathy, clarity, and in a structured, easy-to-read format. "
        "Use markdown for formatting, like lists and bold text. "
        "If a query is outside the health domain, reply: "
        "'❌ I am a Healthcare Expert and can only answer questions related to Health, Fitness, and Diet.' "
        "If someone asks for medical advice or about specific medicines, you MUST refuse and state: "
        "'❌ I am an AI model and cannot provide medical advice, diagnosis, or recommend medication. Please consult a qualified doctor for any medical concerns.'\n\n"
    )

    full_prompt = f"{system_prompt}\n{profile_context}\nUser's Question: {query}"

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        traceback.print_exc() # Print full error to terminal for debugging
        return f"❌ An error occurred while generating the response. Please try again. Error: {e}"

# Button to submit query
if st.button("Generate Health Report"):
    # Create a dictionary to hold all user profile data
    user_profile_data = {
        "age": age,
        "gender": gender,
        "weight": weight,
        "height": height,
        "bmi": bmi_value if bmi_value is not None else 0,
        "activity_level": activity_level,
        "health_goal": health_goal,
        "diet_prefs": diet_prefs,
        "conditions": conditions,
        "allergies": allergies,
        "sleep": sleep,
        "habits": habits
    }
    
    with st.spinner("Analyzing your profile and generating recommendations..."):
        answer = guide_me_on(user_input, user_profile_data)
        st.subheader(":blue[Your Personalized Health Report:]")
        st.markdown(answer)
