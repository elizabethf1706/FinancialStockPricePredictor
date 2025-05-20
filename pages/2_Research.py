import streamlit as st
import base64

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

# Show PDF (must be in the project folder or public URL)
with open("pdfs/your_paper.pdf", "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')

pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>'
st.markdown(pdf_display, unsafe_allow_html=True)
