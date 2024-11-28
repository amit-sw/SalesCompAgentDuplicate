import streamlit as st
from book_appointment import handle_appointment_request, book_appointment

st.title("Appointment Booking System")

# Get available slots
available_slots = handle_appointment_request()

if isinstance(available_slots, str):
    # Show error message if no slots available
    st.error(available_slots)
else:
    # Show dropdown to select time slot
    selected_slot = st.selectbox("Choose an available time slot:", available_slots)
    
    # Get user email
    user_email = st.text_input("Enter your email:")
    
    # Book appointment button
    if st.button("Book Appointment"):
        if user_email:
            result = book_appointment(selected_slot, user_email)
            if "Error" in result:
                st.error(result)
            else:
                st.success(result)
        else:
            st.warning("Please enter your email address")