import streamlit as st
import openai

# Replace with your OpenAI API key
client = openai.OpenAI(api_key="sk-abc123...")  # Replace with your actual OpenAI API key

# Set calorie goal
CALORIE_GOAL = 1800

# Initialize session state
if 'meals' not in st.session_state:
    st.session_state.meals = []
    st.session_state.total_calories = 0

# App title
st.title("📝 Food Accountability Chatbot (GPT-Estimated Calories)")

# Input for meal
meal = st.text_input("What did you eat?")

# Log meal and estimate calories
if st.button("Log Meal"):
    if meal:
        prompt = f"Estimate the total calories for the following meal: {meal}. Just give me the number, no extra text."
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a nutrition expert. Estimate the total calories for a given meal."},
                {"role": "user", "content": prompt}
            ]
        )
        try:
            estimated_calories = int(response.choices[0].message.content.strip())
        except:
            estimated_calories = 0  # Fallback if GPT fails

        st.session_state.meals.append({'meal': meal, 'calories': estimated_calories})
        st.session_state.total_calories += estimated_calories
        st.success(f"Meal added! {meal} - {estimated_calories} kcal. Total calories today: {st.session_state.total_calories}")

# Display meals
if st.session_state.meals:
    st.write("### Today's Meals:")
    for i, entry in enumerate(st.session_state.meals, 1):
        st.write(f"{i}. {entry['meal']} - {entry['calories']} kcal")
    st.write(f"**Total calories:** {st.session_state.total_calories} kcal")

    # GPT feedback
    if st.button("Get Feedback"):
        meal_list = ", ".join([f"{e['meal']} ({e['calories']} kcal)" for e in st.session_state.meals])
        prompt = f"The user has eaten: {meal_list}. Total: {st.session_state.total_calories} kcal. Their goal is {CALORIE_GOAL} kcal for fat loss. Give them feedback."
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a friendly nutrition coach. Help the user stay accountable with their food choices."},
                {"role": "user", "content": prompt}
            ]
        )
        st.write(response.choices[0].message.content)
