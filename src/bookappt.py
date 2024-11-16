import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load credentials
creds = Credentials(
    token=st.secrets['GCALENDAR_ACCESS_TOKEN'],
    refresh_token=st.secrets['GCALENDAR_REFRESH_TOKEN'],
    token_uri='https://oauth2.googleapis.com/token',
    client_id=st.secrets['GCALENDAR_CLIENT_ID'],
    client_secret=st.secrets['GCALENDAR_CLIENT_SECRET'],
    scopes=['https://www.googleapis.com/auth/calendar']
)

def get_calendar_events(event_count=10):
    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=event_count,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")



def add_one_event():
    time_zone = 'America/Los_Angeles'  # Replace with your time zone

    # Event start and end times
    event_start_time = datetime.datetime(2024, 11, 28, 14, 0, 0)  # Year, Month, Day, Hour, Minute, Second
    event_end_time = event_start_time + datetime.timedelta(hours=1)  # Event duration of 1 hour

    # Format event details
    event = {
        'summary': 'Test Appointment - pl ignore',
        'location': '123 Main St, Anytown, USA',
        'description': 'A chance to hear more about our services.',
        'start': {
            'dateTime': event_start_time.isoformat(),
            'timeZone': time_zone,
        },
        'end': {
            'dateTime': event_end_time.isoformat(),
            'timeZone': time_zone,
        },
        'attendees': [
            {'email': 'jaiqbal@paloaltonetworks.com'},  # Replace with the user's email address
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # Email reminder 24 hours before
                {'method': 'popup', 'minutes': 10},        # Popup reminder 10 minutes before
            ],
        },
    }

    try:
        service = build("calendar", "v3", credentials=creds)
        event_result = service.events().insert(
            calendarId='primary',
            body=event,
            sendUpdates='all'
        ).execute()

        print(f"Event created: {event_result.get('htmlLink')}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Streamlit app layout
st.title("Google Form and Calendar Submission")



if st.button("Get Calendar Events"):
    get_calendar_events(10)

if st.button("Add One Event"):
    add_one_event()
