import streamlit as st
from quiz_class import QuizHandler
from gift_recommender_class import GiftRecommender
from calendar_class import CalendarUI

def main():
    st.title("Valentine's Day Planning Suite 💘")

    # Sidebar: Gift Quiz
    with st.sidebar:
        st.header("Partner's Personality Quiz")
        quiz_handler = QuizHandler()
        quiz_handler.handle_quiz_submission()

    # Main Display: Navigation Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Gift Recommender", use_container_width=True):
            st.session_state.current_view = "gift_recommender"
            st.rerun()
    with col2:
        if st.button("Date Planner", use_container_width=True):
            st.session_state.current_view = "calendar"
            st.rerun()

    # Display the selected component
    if st.session_state.get("current_view") == "gift_recommender":
        gift_recommender = GiftRecommender()
        gift_recommender.render(quiz_data=st.session_state.get("responses", {}))

    elif st.session_state.get("current_view") == "calendar":
        calendar = CalendarUI()
        calendar.render(quiz_data=st.session_state.get("responses", {}))

if __name__ == "__main__":
    main()
