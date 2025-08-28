from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import google.generativeai as genai
import traceback
from datetime import date

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
st.set_page_config(page_title="HealthWise", layout="centered")

# ---------------- Main Content ----------------
st.header(":green[HealthWise]–Your Personalized Health Guide 💊", divider="red")

# --- User Profile Inputs in Main Area ---
with st.expander("👤 Enter Your Health Profile for Personalized Results", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Basic Demographics")
        # Date of Birth input
        dob = st.date_input("Date of Birth:", max_value=date.today(), value=date(2000, 1, 1))
        # Calculate age
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        st.write(f"Your age is: **{age}**")
        
        gender = st.selectbox("Gender:", ["Male", "Female", "Other"])

        st.subheader("Lifestyle")
        activity_level = st.selectbox("Activity Level:", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
        health_goal = st.text_input("Primary Health Goal:", placeholder="e.g., Lose Weight, Gain Muscle")
        diet_prefs = st.text_input("Dietary Preferences:", placeholder="e.g., Vegetarian, Vegan")

    with col2:
        st.subheader("⚖️ BMI Calculator")
        weight = st.text_input("Weight (kg):")
        height = st.text_input("Height (cm):")
        bmi_value = None # Initialize BMI value

        try:
            weight_num = pd.to_numeric(weight)
            height_num = pd.to_numeric(height)
            if weight_num > 0 and height_num > 0:
                bmi_value = weight_num / ((height_num / 100) ** 2)
                st.markdown(f"**Your BMI is:** `{bmi_value:.2f}`")
            elif weight and height: # Show info only if both fields are touched
                st.warning("Please enter valid positive numbers.")
        except (ValueError, TypeError):
            if weight or height: # Show info only if user starts typing
                st.info("Enter numerical values to calculate BMI.")

        st.markdown("""
        **BMI Categories:**
        - 🟦 Underweight: BMI < 18.5
        - 🟩 Normal weight: 18.5 ≤ BMI < 25
        - 🟨 Overweight: 25 ≤ BMI < 30
        - 🟥 Obese: BMI ≥ 30
        """)

    st.subheader("Health History (Optional)")
    st.info("Providing these details will result in a much safer and more personalized response.")
    c1, c2 = st.columns(2)
    with c1:
        conditions = st.text_area("Pre-existing Medical Conditions:", placeholder="e.g., Type 2 Diabetes")
        allergies = st.text_area("Known Allergies:", placeholder="e.g., Peanuts, Shellfish")
    with c2:
        sleep = st.text_input("Average Sleep per Night:", placeholder="e.g., 7 hours")
        habits = st.selectbox("Smoking/Alcohol Habits:", ["None", "Occasionally", "Regularly"])

st.markdown("---")

# --- User Query Input ---
user_input = st.text_area("Ask a specific question, or leave blank for a general health report:", height=150)

# Gemini Response Function
def guide_me_on(query, user_profile):
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

    full_prompt = f"{system_prompt}\n{profile_context}\nUser's Request: {query}"

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        traceback.print_exc() # Print full error to terminal for debugging
        return f"❌ An error occurred while generating the response. Please try again. Error: {e}"

# Button to submit query
if st.button("Generate Health Report"):
    # Determine the query to send to the model
    if user_input.strip():
        query_for_gemini = user_input
    else:
        query_for_gemini = "Please provide a general health and wellness report based on my profile. Include advice on diet, exercise, and lifestyle improvements suitable for me."

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
        answer = guide_me_on(query_for_gemini, user_profile_data)
        st.subheader(":blue[Your Personalized Health Report:]")
        st.markdown(answer)
