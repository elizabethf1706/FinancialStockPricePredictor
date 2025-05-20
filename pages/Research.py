import streamlit as st

st.set_page_config(page_title="Research Paper", layout="wide")
st.title("📄 Our Research Paper")

# Section 1: Link to External Paper
st.header("🔗 View the Full Paper Online")
st.write("""
You can access our research paper directly via the following link:
""")
st.markdown("[**Click here to view the paper**](https://docs.google.com/document/d/144SSsXkz2eH5UTeEqTs1iV6tnWswcXmaWkhgZ8LZ9ns/edit?tab=t.0)", unsafe_allow_html=True)

# Section 2: Embedded PDF Viewer
st.header("📑 Embedded PDF Preview")
st.write("You can also read the paper right here:")

# Provide the link to the publicly hosted PDF
pdf_url = "https://your-public-link.com/your_paper.pdf"
st.markdown(f'<iframe src="{pdf_url}" width="100%" height="800px" type="application/pdf"></iframe>', unsafe_allow_html=True)
