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
                # "relationship_type": st.multiselect(
                #     "What are you looking for?",
                #     ["Long-Term relationship", "something casual", "something special", "Not sure yet"],
                #     key="quiz_relationship_type"
                # ),
                # "ideal_date": st.multiselect(
                #     "What's your ideal first date?",
                #     ["Dinner and a movie", "Outdoor adventure", "Coffee and deep conversation", "Fun activity like bowling or mini-golf"]
                # ),
                "gender": st.radio(
                    "What's your partner'sgender?",
                    ["Male", "Female", "Non-Binary", "Other"]
                ),
                "love_language": st.multiselect(
                    "What's your love language?",
                    ["Words of Affirmation", "Acts of Service", "Receiving Gifts", "Quality Time", "Physical Touch"]
                ),
                # "communication_style": st.multiselect(
                #     "How do you prefer to communicate in a relationship?",
                #     ["Frequent texts and calls", "Quality time in person", "Thoughtful gestures", "Give each other space"]
                # ),
                "mbti": st.selectbox(
                    "What's your partner's MBTI type?",
                    ["ENFJ", "ENTJ", "ENTP", "ESFJ", "ESFP", "ESTJ", "ESTP", "INFJ", "INTJ", "INTP", "ISFJ", "ISFP", "ISTJ", "ISTP"],
                    key="quiz_mbti"
                ),
                "diet_preferences": st.multiselect(
                    "What are your diet preferences?",
                    ["Everything", "Vegetarian", "Vegan", "Keto", "Gluten-free", "Halal", "Sattvic"]
                ),
                "drink_preferences": st.multiselect(
                    "What are your drink preferences?",
                    ["Cocktails", "Wines", "Beers", "Spirits", "Non-alcoholic"]
                ),
                "hobbies": st.text_area("What are your favorite hobbies and interests?")
                # "gift_preference": st.radio(
                #     "Do you prefer sentimental or practical gifts?",
                #     ["Sentimental", "Practical", "A mix of both", "Depends on the occasion"]
                # )
            }

            submitted = st.form_submit_button("Submit Responses")

            if submitted:
                st.session_state.responses = responses
                st.session_state.quiz_submitted = True
                st.success("Quiz submitted successfully! 🎉")

