import streamlit as st
import os
from google import genai
from google.genai import types

# Page setup
st.set_page_config(
    page_title="AI Code Reviewer & Security Auditor",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI Code Reviewer & Security Auditor")
st.write("Upload your code file or paste code directly to get an instant security, performance, and quality audit powered by Gemini Flash.")

# Sidebar for API Key configuration
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password", help="Get your API key from Google AI Studio")
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY", "")

# Main layout inputs
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Input Code")
    language = st.selectbox(
        "Select Language", 
        ["Python", "JavaScript / TypeScript", "C / C++", "Java", "Go", "Rust", "PHP", "SQL", "Other"]
    )
    
    uploaded_file = st.file_uploader("Upload a code file", type=["py", "js", "ts", "cpp", "c", "java", "go", "rs", "php", "sql", "txt"])
    
    code_text = ""
    if uploaded_file is not None:
        try:
            code_text = uploaded_file.read().decode("utf-8")
        except Exception as e:
            st.error(f"Error reading file: {e}")
    
    pasted_code = st.text_area("Or paste your code here:", value=code_text, height=350, placeholder="def main():\n    pass")

with col2:
    st.subheader("2. Audit Options")
    focus_areas = st.multiselect(
        "Focus Areas",
        ["Security Vulnerabilities", "Syntax & Logic Bugs", "Performance & Memory", "Code Smells & Readability"],
        default=["Security Vulnerabilities", "Syntax & Logic Bugs", "Performance & Memory", "Code Smells & Readability"]
    )
    
    st.info("⚡ Powered by `gemini-2.5-flash` for rapid analysis.")

# System Instructions / Prompt definition
SYSTEM_PROMPT = """
You are an expert Senior Software Engineer and Cybersecurity Auditor.
Your task is to analyze the provided code snippet and generate a structured audit report.

Evaluate the code based on the following:
1. Overall Quality Score (0 to 100).
2. Security Vulnerabilities (e.g., OWASP top 10, injection risk, insecure memory access).
3. Syntax, Bugs, and Logical Errors.
4. Performance and Optimization issues.
5. Code Smells and Style / Readability Improvements.

Output Format Requirement:
Provide clear Markdown with the following sections:
- **Overall Code Quality Score**: X/100 (Give a short 1-line justification)
- **Key Findings & Vulnerabilities**: Bulleted list of critical or minor issues categorized clearly.
- **Refactored & Optimized Code**: Clean, well-commented code snippet resolving the identified problems.
- **Recommended Next Steps**: Concise actionable tips for the developer.
"""

# Trigger Audit
if st.button("🚀 Run Code Audit", type="primary", use_container_width=True):
    if not api_key:
        st.error("Please provide a valid Gemini API Key in the sidebar.")
    elif not pasted_code.strip():
        st.warning("Please paste or upload code before running the audit.")
    else:
        with st.spinner("Analyzing code for bugs, vulnerabilities, and optimizations..."):
            try:
                # Initialize Gemini Client using google-genai SDK
                client = genai.Client(api_key=api_key)
                
                user_prompt = f"""
                Language: {language}
                Focus Areas: {', '.join(focus_areas)}
                
                Code Snippet:
                ```{language.lower()}
                {pasted_code}
                ```
                """
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.2, # Lower temperature for analytical precision
                    ),
                )
                
                st.success("Audit Complete!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
