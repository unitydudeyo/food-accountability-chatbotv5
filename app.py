# Input for meal
meal = st.text_input("What did you eat?")

# Log meal and estimate calories
if st.button("Log Meal"):
    if meal:
        client = openai.OpenAI(api_key="sk-abc123...")  # Replace with your actual OpenAI API key
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
