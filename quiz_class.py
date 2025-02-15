import streamlit as st

class QuizHandler:
    """Handles the personality quiz for gift recommendations."""

    def __init__(self):
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize session state variables if not already present."""
        if "responses" not in st.session_state:
            st.session_state.responses = {}
        if "quiz_submitted" not in st.session_state:
            st.session_state.quiz_submitted = False

    def handle_quiz_submission(self):

        with st.form("quiz_form"):
            responses = {
                "ideal_date": st.selectbox(
                    "What's your ideal first date?",
                    ["Dinner and a movie", "Outdoor adventure", "Coffee and deep conversation", "Fun activity like bowling or mini-golf"]
                ),
                "love_language": st.selectbox(
                    "What's your love language?",
                    ["Words of Affirmation", "Acts of Service", "Receiving Gifts", "Quality Time", "Physical Touch"]
                ),
                "communication_style": st.radio(
                    "How do you prefer to communicate in a relationship?",
                    ["Frequent texts and calls", "Quality time in person", "Thoughtful gestures", "Give each other space"]
                ),
                "hobbies": st.text_area("What are your favorite hobbies and interests?"),
                "gift_preference": st.radio(
                    "Do you prefer sentimental or practical gifts?",
                    ["Sentimental", "Practical", "A mix of both", "Depends on the occasion"]
                )
            }

            submitted = st.form_submit_button("Submit Responses")

            if submitted:
                st.session_state.responses = responses
                st.session_state.quiz_submitted = True
                st.success("Quiz submitted successfully! 🎉")

