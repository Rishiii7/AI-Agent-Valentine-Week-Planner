# quiz_class.py
import streamlit as st
import openai
from agent_test import generate_product_prompt, agent

class QuizUI:
    def __init__(self):
        """Initialize the QuizUI class"""
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize all required session state variables"""
        if 'responses' not in st.session_state:
            st.session_state.responses = {}
        if 'categories' not in st.session_state:
            st.session_state.categories = []
        if 'gift_suggestions' not in st.session_state:
            st.session_state.gift_suggestions = None
        if 'quiz_submitted' not in st.session_state:
            st.session_state.quiz_submitted = False

    def analyze_personality(self, responses):
        """Analyze user responses and generate gift categories"""
        prompt = f"""
        Based on the following dating personality traits, suggest 3 Amazon product categories that would make the best gifts.

        Traits:
        Ideal Date: {responses.get('ideal_date', '')}
        Love Language: {responses.get('love_language', '')}
        Communication Style: {responses.get('communication_style', '')}
        Hobbies: {responses.get('hobbies', '')}
        Gift Preference: {responses.get('gift_preference', '')}

        Output format: ["Category1", "Category2", "Category3"]
        """
        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            categories = eval(response.choices[0].message.content)
            return categories
        except Exception as e:
            st.error(f"Error analyzing personality: {e}")
            return []

    def get_gift_suggestions(self, categories):
        """Generate gift suggestions based on categories"""
        try:
            prompt = generate_product_prompt(categories)
            response = agent.run(prompt)
            return response.content.strip() if hasattr(response, "content") else "No suggestions available."
        except Exception as e:
            st.error(f"Error generating gift suggestions: {e}")
            return None

    def render(self):
        """Render the quiz interface"""
        st.title("AI-Powered Gift Recommender 🎁")
        st.write("Answer these questions to get AI-generated gift suggestions!")

        # Quiz form
        with st.form("quiz_form"):
            responses = {}
            
            responses['ideal_date'] = st.selectbox(
                "What's your ideal first date?",
                ["Dinner and a movie", "Outdoor adventure", "Coffee and deep conversation", "Fun activity like bowling or mini-golf"]
            )
            
            responses['love_language'] = st.selectbox(
                "What's your love language?",
                ["Words of Affirmation", "Acts of Service", "Receiving Gifts", "Quality Time", "Physical Touch"]
            )
            
            responses['communication_style'] = st.radio(
                "How do you prefer to communicate in a relationship?",
                ["Frequent texts and calls", "Quality time in person", "Thoughtful gestures", "Give each other space"]
            )

            responses['hobbies'] = st.text_area("What are your favorite hobbies and interests?")

            responses['gift_preference'] = st.radio(
                "Do you prefer sentimental or practical gifts?",
                ["Sentimental", "Practical", "A mix of both", "Depends on the occasion"]
            )

            submitted = st.form_submit_button("Submit Responses")
            
            if submitted:
                st.session_state.responses = responses
                st.session_state.quiz_submitted = True
                
                with st.spinner("Analyzing your preferences..."):
                    # Get categories
                    categories = self.analyze_personality(responses)
                    st.session_state.categories = categories
                    
                    # Display categories
                    if categories:
                        st.success("Quiz completed successfully! 🎉")
                        st.subheader("Suggested Gift Categories:")
                        for category in categories:
                            st.write(f"🎁 {category}")
                        
                        # Get and display gift suggestions
                        with st.spinner("Generating gift suggestions..."):
                            suggestions = self.get_gift_suggestions(categories)
                            if suggestions:
                                st.session_state.gift_suggestions = suggestions
                                st.subheader("Gift Suggestions:")
                                st.markdown(suggestions)

        # Display results if already submitted
        if st.session_state.quiz_submitted and not submitted:
            if st.session_state.categories:
                st.subheader("Your Suggested Gift Categories:")
                for category in st.session_state.categories:
                    st.write(f"🎁 {category}")
            
            if st.session_state.gift_suggestions:
                st.subheader("Your Gift Suggestions:")
                st.markdown(st.session_state.gift_suggestions)

            # Add a refresh button for new suggestions
            if st.button("Get New Suggestions"):
                with st.spinner("Generating new gift suggestions..."):
                    suggestions = self.get_gift_suggestions(st.session_state.categories)
                    if suggestions:
                        st.session_state.gift_suggestions = suggestions
                        st.experimental_rerun()

        return st.session_state.quiz_submitted