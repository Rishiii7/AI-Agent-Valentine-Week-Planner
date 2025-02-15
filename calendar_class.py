import streamlit as st
from agno.agent import Agent
from agno.tools.googlecalendar import GoogleCalendarTools
from agno.tools.google_maps import GoogleMapTools
import requests
import json

class CalendarUI:
    def __init__(self):
        self.user_location = self.get_user_location()
        self.agent = self.initialize_agent()
        if "ai_suggestion" not in st.session_state:
            st.session_state.ai_suggestion = None

    def get_user_location(self):
        """Get user's location using IP-based geolocation"""
        try:
            response = requests.get('https://ipapi.co/json/')
            if response.status_code == 200:
                data = response.json()
                return {
                    'city': data.get('city', ''),
                    'region': data.get('region', ''),
                    'country': data.get('country_name', ''),
                    'latitude': data.get('latitude', ''),
                    'longitude': data.get('longitude', '')
                }
        except Exception as e:
            st.warning(f"Could not determine location automatically: {str(e)}")
        return None

    def initialize_agent(self):
        location_context = ""
        if self.user_location:
            location_context = f"\nUser's current location: {self.user_location['city']}, {self.user_location['region']}, {self.user_location['country']}"
        return Agent(
            tools=[
                GoogleMapTools(),
                GoogleCalendarTools(credentials_path="token.json")
            ],
            instructions=[
                f"""
                You are an expert Valentine's Day planner. Your job is to suggest a perfect date plan that includes:
                1. A **specific activity** (e.g., romantic dinner, movie night, outdoor adventure, surprise gift).
                2. A **recommended time** for the event that ensures the best experience.
                3. A **location** based on the user's input, or if unavailable, access the user's current location and suggest a venue within a **20-mile radius**.
                4. **Ensure the event does not conflict** with the user's existing Google Calendar events.

                Ensure the output follows this structured format:

                **Event**: Sunset Rooftop Dinner  
                **Date**: February 14, 2025  
                **Time**: 7:00 PM - 9:00 PM  
                **Location**: 17 Barrow St, New York, NY   

                From the  user's location from {location_context} to find an ideal venue within a **20-mile radius**.

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
        
        return details["Event"], details["Date"], details["Time"], details["Location"]
    
    def render(self, quiz_data):
        st.title("💖 Valentine's Week Planner 💖")
        st.write("Plan your perfect Valentine's Week with Google Calendar integration!")
        try:
            response = self.agent.run(f"Suggest a perfect Valentine's plan based on: {quiz_data} and in location: {self.user_location}")
            st.session_state.ai_suggestion = response.content.strip()

            if st.session_state.ai_suggestion:
                st.subheader("✨ AI Suggestion:")
                st.write(st.session_state.ai_suggestion)
            else:
                st.error("Failed to generate AI suggestions. Please try again.")
        except Exception as e:
            st.error(f"Error generating AI suggestion: {e}")
        
        if st.button("Add to Google Calendar"):
            ai_suggestion = st.session_state.ai_suggestion
            
            if not ai_suggestion:
                st.error("Please generate an AI suggestion before adding it to the calendar.")
            else:
                try:
                    event_title, event_date, event_time, location = self.parse_event_details(ai_suggestion)
                    
                    if not all([event_title, event_date, event_time, location]):
                        st.error("AI response is incomplete. Please regenerate suggestions.")
                    else:
                        self.agent.run(f'create a calendar event with title "{event_title}", date "{event_date}", time "{event_time}", and location "{location}"')
                        st.success(f"AI Suggested Event '{event_title}' added to Google Calendar!")
                except Exception as e:
                    st.error(f"Failed to add AI suggestion to Google Calendar: {e}")
