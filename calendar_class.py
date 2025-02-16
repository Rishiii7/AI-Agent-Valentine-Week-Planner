import streamlit as st
from agno.agent import Agent
from agno.tools.googlecalendar import GoogleCalendarTools
from agno.tools.google_maps import GoogleMapTools
import requests
from datetime import date

class CalendarUI:
    def __init__(self):
        self.user_location = self.get_user_location()
        self.agent = self.initialize_agent()
        
        # Initialize session state variables
        if "ai_suggestion" not in st.session_state:
            st.session_state.ai_suggestion = None
        if "event_added" not in st.session_state:
            st.session_state.event_added = False

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
        
        current_date = date.today().strftime('%Y-%m-%d')
        return Agent(
            tools=[
                GoogleMapTools(),
                GoogleCalendarTools(credentials_path="token.json")
            ],
            instructions=[
                f"""
                You are an expert Valentine's Day planner. Your job is to suggest a perfect date plan that includes:
                1. A **specific activity** (e.g., romantic dinner, movie night, outdoor adventure, surprise gift).
                2. A **recommended time** for the event that:
                   - Must be scheduled from {current_date} onwards (today or future dates only)
                   - Should be during appropriate hours for the activity (e.g., dinner during dinner time)
                   - Must not conflict with the user's existing Google Calendar events
                3. A **location** based on the user's input, or if unavailable, access the user's current location and suggest a venue within a **20-mile radius**.

                Before suggesting a time:
                1. First check the user's Google Calendar for any existing events
                2. Find a suitable time slot that doesn't conflict with their schedule
                3. Consider the type of activity and appropriate timing

                Ensure the output follows this structured format:

                **Event**: [Activity Name]  
                **Date**: [YYYY-MM-DD] (must be {current_date} or later)  
                **Time**: [HH:MM AM/PM - HH:MM AM/PM]  
                **Location**: [Full Address]   

                From the user's location from {location_context} to find an ideal venue within a **20-mile radius**. 

                Suggest only **one** event that matches user preferences. Keep it **concise** and **actionable**.
                """
            ],
            add_datetime_to_instructions=True,
            structured_outputs=True
        )
    
    def parse_event_details(self, ai_suggestion):
        """Extract event details from AI response"""
        details = {"Event": "", "Date": "", "Time": "", "Location": ""}
        for line in ai_suggestion.split("\n"):
            for key in details.keys():
                if line.startswith(f"**{key}**"):
                    details[key] = line.split(":", 1)[1].strip()
        return details["Event"], details["Date"], details["Time"], details["Location"]
    
    def generate_ai_suggestion(self, quiz_data):
        """Generate AI suggestion and store it in session state"""
        if not st.session_state.ai_suggestion:
            try:
                # Proactively check calendar conflicts
                conflicts = self.agent.run("Check calendar for conflicts next week")
                
                # Get weather forecast
                weather = self.agent.run("Get weather forecast for potential dates")
                
                # Generate personalized suggestion
                response = self.agent.run(
                    f"""
                    Generate a date plan considering:
                    1. Calendar conflicts: {conflicts}
                    2. Weather forecast: {weather}
                    3. User preferences: {quiz_data}
                    4. Location: {self.user_location}
                    5. Current date: {date.today().strftime('%Y-%m-%d')}
                    """
                )
                # response = self.agent.run(f"Suggest a perfect Valentine's plan based on user preference: {quiz_data}, in location: {self.user_location} and time: {date.today().strftime('%Y-%m-%d')}")
                st.session_state.ai_suggestion = response.content.strip()
            except Exception as e:
                st.error(f"Error generating AI suggestion: {e}")
    
    def add_event_to_calendar(self):
        """Add event to Google Calendar without regenerating the AI suggestion"""
        ai_suggestion = st.session_state.ai_suggestion
        
        if not ai_suggestion:
            st.error("Please generate an AI suggestion before adding it to the calendar.")
            return

        try:
            event_title, event_date, event_time, location = self.parse_event_details(ai_suggestion)
            
            if not all([event_title, event_date, event_time, location]):
                st.error("AI response is incomplete. Please regenerate suggestions.")
                return

            self.agent.run(f'create a calendar event with title "{event_title}", date "{event_date}", time "{event_time}", and location "{location}"')
            st.session_state.event_added = True
            st.success(f"✅ AI Suggested Event '{event_title}' added to Google Calendar!")
        except Exception as e:
            st.error(f"Failed to add AI suggestion to Google Calendar: {e}")
    
    def render(self, quiz_data):
        st.title("💖 Valentine's Week Planner 💖")

        self.generate_ai_suggestion(quiz_data)

        if st.session_state.ai_suggestion:
            st.subheader("✨ AI Suggestion:")
            st.write(st.session_state.ai_suggestion)
        else:
            st.error("Failed to generate AI suggestions. Please try again.")

        # Prevent Re-execution of render() on button click
        if not st.session_state.event_added:
            if st.button("Add to Google Calendar"):
                self.add_event_to_calendar()
        else:
            st.success("🎉 Event has already been added to Google Calendar!")
