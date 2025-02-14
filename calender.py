import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
print(os.environ["OPENAI_API_KEY"])
import pickle
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set your OpenAI API key

# Google Calendar API credentials file
CLIENT_SECRET_FILE = 'client_secret_418230902377-2v2j84in50ct5jm216139mlqpbpmh5r8.apps.googleusercontent.com.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Authenticate Google Calendar API
def authenticate_google_account():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build(API_NAME, API_VERSION, credentials=creds)
    return service

# Create event in Google Calendar
def create_google_event(service, event_title, event_start, event_end, event_description=None):
    event = {
        'summary': event_title,
        'location': '',
        'description': event_description,
        'start': {
            'dateTime': event_start,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': event_end,
            'timeZone': 'America/New_York',
        },
        'reminders': {
            'useDefault': True,
        },
    }

    try:
        event_result = service.events().insert(
            calendarId='primary', body=event).execute()
        print(f"Event created: {event_result.get('htmlLink')}")
    except HttpError as error:
        print(f"An error occurred: {error}")

# Use GPT-4 to parse and generate event details
def parse_event_request(event_request):
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an AI assistant that extracts event details (title, date, and time) from user messages."},
        {"role": "user", "content": f"Extract the date, time, and event details from this request: '{event_request}'. Return output in this format: 'Event: <title>, Date: <YYYY-MM-DD>, Time: <HH:MM>'"}
    ],
    temperature=0.5)

    result = response.choices[0].message.content.strip()
    # print(result)
    return result

def main():
    # Authenticate and build the Google Calendar API service
    service = authenticate_google_account()

    # Input from user (This can be more dynamic based on AI interpretation)
    user_input = input("What event would you like to add to your calendar? \n-> ")

    # Get event details from GPT-4
    event_details = parse_event_request(user_input)
    print(event_details)
    # Extract start time, end time, and event title from the parsed result
    try:
        details = {}
        for item in event_details.split(","):
            k,v = item.split(":", 1)
            print(k.strip(), v.strip())
            details[k.strip()] = v.strip()

        # details = {k.strip(): v.strip() for k, v = item.split(":") for item in event_details.split(",")}
        print(details)
        event_title = details.get("Event")
        event_date = details.get("Date")
        event_time = details.get("Time")
        print(event_title, event_date, event_time)

        event_start = datetime.datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M")
        event_end = event_start + datetime.timedelta(hours=1)  # Default event length 1 hour

        # Create the event in Google Calendar
        create_google_event(service, event_title, event_start.isoformat(), event_end.isoformat())

    except Exception as e:
        print("Error processing event details:", e)

if __name__ == '__main__':
    main()
