"""
For multiple pages:
1. create entry point (app.py) 
2. Each page has its own python file
3a. st.Page to define, 
3b. st.navigation to connect pages
"""

import streamlit as st

login_page = st.Page("login_page.py", title="Login Page", icon="🎈")
home_page = st.Page("home_page.py", title="Home Page")

pages = st.navigation([login_page, home_page])

# const globals for page names
st.session_state["stock_search_page"] = "get_stock_page.py"
st.session_state["finance_analysis_page"] = "finance_analysis.py"
#st.session_state["stock"] = ""


pages.run()
