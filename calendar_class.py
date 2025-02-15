# calendar_class.py
import streamlit as st
from agno.agent import Agent
from agno.tools.googlecalendar import GoogleCalendarTools
from agno.tools.google_maps import GoogleMapTools

class CalendarUI:
    def __init__(self):
        self.agent = self.initialize_agent()

    def initialize_agent(self):
        return Agent(
            tools=[
                GoogleMapTools(),
                GoogleCalendarTools(credentials_path="token.json")
            ],
            instructions=[
                """
                You are an expert Valentine's Day planner. Your job is to suggest a perfect date plan that includes:
                1. A **specific activity**
                2. A **recommended time**
                3. A **location**
                4. **Ensure no calendar conflicts**

                Output format:
                **Event**: [Event Name]
                **Date**: [Date]
                **Time**: [Time]
                **Location**: [Location]

                If the user **has not provided a location**, use their **current location** to find an ideal venue within a **20-mile radius**.

                Suggest only **one** event that matches user preferences. Keep it **concise** and **actionable**.
                """
            ],
            add_datetime_to_instructions=True,
            structured_outputs=True
        )

    def parse_event_details(self, ai_suggestion):
        details = {"Event": "", "Date": "", "Time": "", "Location": ""}
        for line in ai_suggestion.split("\n"):
            for key in details.keys():
                if line.startswith(f"**{key}**"):
                    details[key] = line.split(":", 1)[1].strip()
        return details

    def render(self):
        st.title("💖 Valentine's Week Planner 💖")
        
        # Google Authentication
        if st.button("Authenticate with Google Calendar"):
            try:
                gcal = GoogleCalendarTools(credentials_path="client_secret.json")
                gcal.authenticate()
                st.success("Authenticated successfully!")
            except Exception as e:
                st.error(f"Authentication failed: {e}")

        # User Input
        preferences = st.text_area("Tell us about your Valentine's preferences")
        
        if st.button("Get AI Suggestions"):
            try:
                response = self.agent.run(f"Suggest a perfect Valentine's plan based on: {preferences}")
                ai_suggestion = response.content.strip()
                st.session_state.ai_suggestion = ai_suggestion
                st.subheader("✨ AI Suggestion:")
                st.write(ai_suggestion)
            except Exception as e:
                st.error(f"Error generating AI suggestion: {e}")

        # Add to Calendar
        if st.button("Add to Google Calendar"):
            if 'ai_suggestion' not in st.session_state:
                st.error("Please generate an AI suggestion first.")
            else:
                try:
                    details = self.parse_event_details(st.session_state.ai_suggestion)
                    self.agent.run(
                        f'create a calendar event with title "{details["Event"]}", '
                        f'date "{details["Date"]}", time "{details["Time"]}", '
                        f'location "{details["Location"]}"'
                    )
                    st.success(f"Event '{details['Event']}' added to Google Calendar!")
                except Exception as e:
                    st.error(f"Failed to add event to calendar: {e}")