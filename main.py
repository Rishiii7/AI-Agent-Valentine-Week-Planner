# main.py
import streamlit as st
from quiz_class import QuizUI
from calendar_class import CalendarUI

def main():
    st.title("Valentine's Day Planning Suite 💘")
    
    # Initialize classes
    quiz = QuizUI()
    calendar = CalendarUI()
    
    # Initialize session state
    if 'current_view' not in st.session_state:
        st.session_state.current_view = None

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Gift Quiz", use_container_width=True):
            st.session_state.current_view = "quiz"
            st.rerun()
    with col2:
        if st.button("Date Planner", use_container_width=True):
            st.session_state.current_view = "calendar"
            st.rerun()

    # Render current view
    if st.session_state.current_view == "quiz":
        quiz.render()
    elif st.session_state.current_view == "calendar":
        calendar.render()
    else:
        st.write("👆 Select an option above to get started!")

    # Display gift suggestions in calendar view if available
    if st.session_state.current_view == "calendar" and 'gift_suggestions' in st.session_state:
        with st.expander("View Your Gift Suggestions"):
            st.markdown(st.session_state.gift_suggestions)

if __name__ == "__main__":
    main()