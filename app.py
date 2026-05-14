import streamlit as st
import joblib
import numpy as np
import pandas as pd
from chatbot_logic import chatbot_response
from diet_plan import generate_plan
from io import StringIO

# --- Banner and Title ---
st.markdown("<h1 style='text-align: center; color: green;'>🍎 Nutrition App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your personal guide to healthy eating</p>", unsafe_allow_html=True)

st.image(
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
    width=800
)

# --- Load model ---
model = joblib.load('calorie_predictor.pkl')

# --- Sidebar ---
st.sidebar.title("🍊 Nutrition Tips")
st.sidebar.info("Stay hydrated and include more fruits & veggies in your meals!")

choice = st.sidebar.radio(
    "Choose a feature:",
    ["Diet Plan", "FAQ Chatbot","Calorie Predictor"]
)

# --- Custom CSS ---
st.markdown("""
    <style>
    .section {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .predictor {
        background-color: #e8f5e9;
    }
    .chatbot {
        background-color: #e3f2fd;
    }
    .dietplan {
        background-color: #fff3e0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Calorie Predictor ---
if choice == "Calorie Predictor":
    st.markdown("<div class='section predictor'>", unsafe_allow_html=True)
    st.header("Calorie Prediction")

    protein = st.number_input("Protein (g)", min_value=0.0)
    carbs = st.number_input("Carbs (g)", min_value=0.0)
    fats = st.number_input("Fats (g)", min_value=0.0)

    if st.button("Predict Calories"):
        input_data = np.array([[protein, carbs, fats]])
        prediction = model.predict(input_data)
        st.success(f"Estimated Calories: {prediction[0]:.2f}")

    st.markdown("</div>", unsafe_allow_html=True)

# --- FAQ Chatbot ---
elif choice == "FAQ Chatbot":
    st.markdown("<div class='section chatbot'>", unsafe_allow_html=True)
    st.header("Nutrition FAQ Chatbot")

    user_query = st.text_input("Ask a nutrition question:")

    if st.button("Get Answer"):

        result = chatbot_response(user_query)

        # --- USER ---
        st.markdown(f"**You:** {user_query}")

        # --- BOT TEXT ---
        st.markdown(f"**Bot:** {result['text']}")

        # --- TABLE (if exists) ---
        if result["table"] is not None:
            st.markdown("### Recommended foods:")
            st.dataframe(result["table"])

    st.markdown("</div>", unsafe_allow_html=True)

# --- Diet Plan ---
elif choice == "Diet Plan":
    st.markdown("<div class='section dietplan'>", unsafe_allow_html=True)
    st.header("Personalized Diet Plan")

    weight = st.number_input("Current Weight (kg)", min_value=30.0)
    goal = st.selectbox("Goal", ["Lose Weight", "Gain Weight", "Maintain"])
    duration = st.slider("Duration (weeks)", 1, 4, 2)

    if st.button("Generate Plan"):
        plan = generate_plan(weight, goal, duration)
        df = pd.DataFrame(plan)

        st.markdown("### 🥗 Your Personalized Diet Plan")
        st.dataframe(df)

        # Download option
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Diet Plan as CSV",
            data=csv,
            file_name='diet_plan.csv',
            mime='text/csv',
        )

    st.markdown("</div>", unsafe_allow_html=True)