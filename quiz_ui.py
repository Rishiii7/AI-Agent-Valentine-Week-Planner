from turtle import onclick
import streamlit as st
import openai
from agent_test import generate_product_prompt, agent
import uuid
import os

# Set up OpenAI API Key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Function to call GPT for personality analysis
def analyze_personality(responses):
    prompt = f"""
    Based on the following dating personality traits, suggest 3 Amazon product categories that would make the best gifts.

    Traits:
    {responses}

    Output format: ["Category1", "Category2", "Category3"]
    """

    # client = openai.OpenAI(api_key=OPENAI_API_KEY)
    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
    )

    categories = response.choices[0].message.content

    try:
        categories = eval(categories)  # Ensure the response is a valid Python list
    except:
        st.error("Error converting response to list. Please try again.")
        return []

    return categories

# Function to get user quiz responses
def get_quiz_responses():
    st.title("AI-Powered Gift Recommender 🎁")
    st.write("Answer these questions to get AI-generated gift suggestions!")

    responses = {}

    # Quiz questions
    responses['ideal_date'] = st.selectbox("What’s your ideal first date?", 
                                          ["Dinner and a movie", "Outdoor adventure", "Coffee and deep conversation", "Fun activity like bowling or mini-golf"],
                                          key="quiz_ideal_date")
    
    responses['love_language'] = st.selectbox("What’s your love language?", 
                                             ["Words of Affirmation", "Acts of Service", "Receiving Gifts", "Quality Time", "Physical Touch"],
                                             key="quiz_love_language")
    
    responses['communication_style'] = st.radio("How do you prefer to communicate in a relationship?", 
                                               ["Frequent texts and calls", "Quality time in person", "Thoughtful gestures", "Give each other space"],
                                               key="quiz_communication_style")

    responses['hobbies'] = st.text_area("What are your favorite hobbies and interests?", key="quiz_hobbies")

    responses['gift_preference'] = st.radio("Do you prefer sentimental or practical gifts?", 
                                           ["Sentimental", "Practical", "A mix of both", "Depends on the occasion"],
                                           key="quiz_gift_preference")

    if st.button("Submit Responses"):
        st.success("Thank you for completing the quiz! 🎁")
        st.session_state['responses'] = responses
        st.session_state['categories'] = analyze_personality(responses)  # Store categories
        print(st.session_state['categories'])
        st.session_state['fetch_new_products'] = True  # Ensure we fetch products
        st.rerun()  # Rerun the app to fetch suggestions
 
    # return st.session_state.get('responses', {})

# Function to fetch and display gift suggestions
def get_gift_suggestions():
    # Fetches and displays gift suggestions
    if 'categories' not in st.session_state or not st.session_state['categories']:
        return

    categories = st.session_state['categories']
    st.subheader("🎁 Suggested Gift Categories")
    for category in categories:
        st.write(f"🛍️ **{category}**")

    if 'fetch_new_products' in st.session_state and st.session_state['fetch_new_products']:
        prompt = generate_product_prompt(categories)

        with st.spinner("Fetching products..."):
            response = agent.run(prompt)

        final_output = response.content.strip() if hasattr(response, "content") and response.content else "No content received."
        st.session_state['gift_suggestions'] = final_output
        st.session_state['fetch_new_products'] = False  # Prevent infinite looping
        st.rerun()  # Rerun the UI to display the results

    if 'gift_suggestions' in st.session_state:
        st.subheader("🎯 AI-Powered Gift Suggestions")
        st.markdown(st.session_state['gift_suggestions'], unsafe_allow_html=True)

        # Feedback Section
        feedback = st.selectbox("Are you satisfied with these suggestions?", ["Select an option", "Yes", "No"], key="feedback")

        if feedback == "Yes":
            st.session_state.clear()  # Reset session state to restart quiz
            st.rerun()

        elif feedback == "No":
            st.session_state['fetch_new_products'] = True  # Fetch new products but keep same categories
            st.rerun()


# Streamlit App
def main():
    get_quiz_responses()
    get_gift_suggestions() 

if __name__ == "__main__":
    main()
