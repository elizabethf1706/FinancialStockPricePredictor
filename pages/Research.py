import streamlit as st

st.set_page_config(page_title="Research Paper", layout="wide")
st.title("📄 Our Research Paper")

# Section 1: Link to External Paper
st.header("🔗 View the Full Paper Online")
st.write("""
You can access our research paper directly via the following link:
""")
st.markdown("[**Click here to view the paper**](https://docs.google.com/document/d/e/2PACX-1vRVf58-LPlKMAQZW1FkBP9KRcauFAKUjPzU5Tc2UJYvl6GIlA1EOSK9YvrC06Isc2TeCrgo6ygxDJhL/pub)", unsafe_allow_html=True)

# Section 2: Embed the Google Doc (Embedded Preview)
st.header("📑 Embedded Research Paper")
st.write("You can also read the paper right here:")

# Embed the document using the published URL
iframe_code = """
<iframe src="https://docs.google.com/document/d/e/2PACX-1vRVf58-LPlKMAQZW1FkBP9KRcauFAKUjPzU5Tc2UJYvl6GIlA1EOSK9YvrC06Isc2TeCrgo6ygxDJhL/pub" width="100%" height="800px"></iframe>
"""
st.markdown(iframe_code, unsafe_allow_html=True)
