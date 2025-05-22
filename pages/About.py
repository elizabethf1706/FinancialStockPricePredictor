# About Me Page will include meet the team intro and purpose of website application
import streamlit as st

st.title("About Me")

col1, col2 = st.columns(2)

with col1:
    st.header("Our Purpose")
    st.write("""
    This application serves as a tool for stock market traders and financial analysts.\n
    It guides market professionals in making more informed decisions when investing, buying, and selling.\n
    Our team built this web app in just 6 weeks, and we are excited to continue improving it!
    """)
with col2: 
    st.header("What we Offer")
    st.write("""
    1. AI and machine learning forecasting models\n
    2. Current news headliners\n
    3. Sentiment analysis\n
    4. Generated wordcloud\n
    5. Applicable charts\n
    6. AI-powered earnings insights
    """)

st.header("Meet the Team")

# Team member info
team = [
    {"name": "Elizabeth Flynn", "role": "Project Lead", "image": "images/Elizabeth.png"},
    {"name": "Kevin Gerges", "role": "Backend", "image": "images/Kevin.png"},
    {"name": "Stephanie Manalo", "role": "Designer", "image": "images/Stephanie.png"},
    {"name": "Christopher Osgood", "role": "Designer", "image": "images/Christopher.jpg"},
    {"name": "Kleber Ordonez", "role": "Designer", "image": "images/Kleber2.png"},
    {"name": "Jasper Garcia", "role": "Designer", "image": "images/Jasper.png"},
]

# Function to split the team into chunks of size n
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# For each chunk of 3 members, create 3 columns
for chunk in chunks(team, 3):
    cols = st.columns(3)
    for col, member in zip(cols, chunk):
        with col:
            st.image(member["image"], caption=f"{member['name']} - {member['role']}", width=150)
  

st.header("Special Thanks to:")
# Anuj Shoutout
mentor = [
    {"name": "Anuj Sainj", "role": "Project Mentor", "image": "images/Anuj.png"}
]
for person in mentor:
    st.image(person["image"], caption=f"{person['name']} - {person['role']}", width=150)
