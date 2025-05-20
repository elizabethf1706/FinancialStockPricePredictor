import streamlit as st

st.set_page_config(page_title="Contact Us", layout="centered")

st.title("📬 Contact Us")

st.write("""
We'd love to hear from you!  
Fill out the form below and we’ll get back to you as soon as possible.
""")

with st.form(key="contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message", height=150)
    submit = st.form_submit_button("Send Message")

    if submit:
        if name and email and message:
            st.success(f"Thank you, {name}! Your message has been sent.")
            # You could add code here to send the message via email or store it
        else:
            st.error("Please fill out all fields before submitting.")
