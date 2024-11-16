# Import required libraries
import streamlit as st  # For creating web interface
from google.oauth2 import service_account
from googleapiclient.discovery import build  # For interacting with Google APIs
import datetime
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Initialize Google Calendar API credentials using Streamlit secrets
# These credentials are stored securely in Streamlit's secrets management
creds = Credentials(
    token=st.secrets['GCALENDAR_ACCESS_TOKEN'],
    refresh_token=st.secrets['GCALENDAR_REFRESH_TOKEN'],
    token_uri='https://oauth2.googleapis.com/token',
    client_id=st.secrets['GCALENDAR_CLIENT_ID'],
    client_secret=st.secrets['GCALENDAR_CLIENT_SECRET'],
    scopes=['https://www.googleapis.com/auth/calendar']  # Specify access level needed
)

def get_calendar_events(event_count=10):
    """
    Fetch upcoming calendar events from Google Calendar
    Args:
        event_count (int): Number of events to retrieve (default: 10)
    """
    try:
        # Create Google Calendar API service
        service = build("calendar", "v3", credentials=creds)

        # Get current time in UTC format
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        
        # Query the Calendar API for upcoming events
        events_result = (
            service.events()
            .list(
                calendarId="primary",  # Use primary calendar
                timeMin=now,           # Only get future events
                maxResults=event_count,
                singleEvents=True,     # Don't include recurring events
                orderBy="startTime",   # Sort by start time
            )
            .execute()
        )
        events = events_result.get("items", [])

        # Handle case when no events are found
        if not events:
            print("No upcoming events found.")
            return

        # Display event details
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")

def add_one_event():
    """
    Add a single test event to Google Calendar
    """
    # Set timezone for the event
    time_zone = 'America/Los_Angeles'

    # Define event timing
    event_start_time = datetime.datetime(2024, 11, 28, 14, 0, 0)  # Year, Month, Day, Hour, Minute, Second
    event_end_time = event_start_time + datetime.timedelta(hours=1)  # Event duration of 1 hour

    # Create event details dictionary
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
            {'email': 'jaiqbal@paloaltonetworks.com'},  # Attendee email
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # Email reminder 24 hours before
                {'method': 'popup', 'minutes': 10},       # Popup reminder 10 minutes before
            ],
        },
    }

    try:
        # Create Google Calendar API service
        service = build("calendar", "v3", credentials=creds)
        
        # Insert the event into the calendar
        event_result = service.events().insert(
            calendarId='primary',
            body=event,
            sendUpdates='all'  # Send email updates to all attendees
        ).execute()

        print(f"Event created: {event_result.get('htmlLink')}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Create Streamlit web interface
st.title("Google Form and Calendar Submission")

# Add buttons for calendar operations
if st.button("Get Calendar Events"):
    get_calendar_events(10)

if st.button("Add One Event"):
    add_one_event()
