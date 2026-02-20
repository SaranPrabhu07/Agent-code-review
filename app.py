import streamlit as st
from google import genai
import os

# Page Config
st.set_page_config(page_title="AI Code Reviewer", page_icon="🤖")

st.title("🤖 AI Code Review Gatekeeper")
st.markdown("""
Paste your code changes below to see how the **DevOps AI Agent** reviews your work!
""")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    model_choice = st.selectbox("Choose Model", ["gemini-2.5-flash", "gemini-3-flash-preview"])

# Input Area
code_input = st.text_area("Paste your Git Diff or Code here:", height=300, placeholder="def my_function():\n    api_key = '12345'...")

if st.button("Analyze Code"):
    if not api_key:
        st.error("Please provide an API Key in the sidebar!")
    elif not code_input:
        st.warning("Please paste some code first.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            with st.spinner("Senior Engineer is reviewing..."):
                prompt = f"Review this code for security and logic errors. Output a Markdown table:\n\n{code_input}"
                response = client.models.generate_content(
                    model=model_choice,
                    contents=prompt
                )
                
                # Show results
                st.subheader("Review Report")
                st.markdown(response.text)
                
                if "REJECT" in response.text.upper():
                    st.error("❌ STATUS: REJECTED")
                else:
                    st.success("✅ STATUS: PASSED")
                    
        except Exception as e:
            st.error(f"An error occurred: {e}")
