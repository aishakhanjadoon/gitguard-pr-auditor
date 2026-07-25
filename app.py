import json
import streamlit as st
from openai import OpenAI

# Page Config
st.set_page_config(
    page_title="GitGuard - AI PR & Code Risk Auditor",
    page_icon="🛡️",
    layout="wide"
)

# Sidebar - Configuration & Credentials
with st.sidebar:
    st.title("🛡️ GitGuard Config")
    # Updated label & help text for Groq
    api_key = st.text_input(
        "Groq API Key", 
        type="password", 
        help="Get your 100% free API key from console.groq.com"
    )
    st.markdown("---")
    st.markdown("### About")
    st.info("GitGuard helps developers audit raw code diffs or Pull Requests before merging, detecting safety risks and missing test cases in seconds.")

# Main Header
st.title("🛡️ GitGuard: AI Code Auditor & PR Assistant")
st.caption("Identify security risks, analyze breaking changes, and generate unit test stubs instantly.")

# Input Section
st.subheader("1. Paste Code Diff or Modified Function")
code_input = st.text_area(
    "Paste your 'git diff' output or source code here:",
    height=200,
    placeholder="def calculate_total(items):\n    # TODO: Add validation\n    return sum(item.price for item in items)"
)

# Session State Initializers
if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "test_stubs" not in st.session_state:
    st.session_state.test_stubs = None

# Action Button
if st.button("🚀 Run AI Safety Audit", type="primary", use_container_width=True):
    if not api_key:
        st.error("Please enter your free Groq API key in the sidebar.")
    elif not code_input.strip():
        st.warning("Please paste some code or diff to analyze.")
    else:
        with st.status("🔍 Auditing code base...", expanded=True) as status:
            try:
                # Point OpenAI client to Groq's endpoint
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.groq.com/openai/v1"
                )
                
                system_prompt = """
                You are a Senior Security Auditor and QA Architect.
                Analyze the code/diff provided and return a JSON object with EXACTLY these keys:
                - "change_type": One of ["Refactor", "Feature", "Fix", "Security Bug", "Breaking Change"]
                - "pr_title": Concise Conventional Commit title
                - "pr_body": Detailed markdown summary of changes and potential bugs
                - "missing_tests": Array of strings describing specific missing test scenarios
                - "risk_score": Integer from 1 (Safe) to 10 (Critical Risk)
                """
                
                # Using Llama 3.3 70B via Groq
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    temperature=0.2,
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Analyze this code:\n\n{code_input}"}
                    ]
                )
                
                st.session_state.analysis = json.loads(response.choices[0].message.content)
                st.session_state.test_stubs = None
                status.update(label="Audit Complete!", state="complete", expanded=False)
            except Exception as e:
                st.error(f"Audit failed: {e}")

# Display Results Dashboard
if st.session_state.analysis:
    data = st.session_state.analysis
    st.markdown("---")
    
    # Visual Metrics Row
    col1, col2, col3 = st.columns(3)
    risk = int(data.get("risk_score", 1))
    
    with col1:
        st.metric(
            label="Security Risk Score", 
            value=f"{risk} / 10",
            delta="High Risk!" if risk >= 7 else "Safe",
            delta_color="inverse" if risk >= 7 else "normal"
        )
    with col2:
        st.metric(label="Change Classification", value=data.get("change_type", "Unknown"))
    with col3:
        st.metric(label="Missing Test Scenarios", value=len(data.get("missing_tests", [])))

    st.markdown("---")

    # PR Details
    st.subheader("📝 Suggested Pull Request")
    st.code(data.get("pr_title", ""), language="text")
    
    with st.expander("📄 View Full PR Description", expanded=True):
        st.markdown(data.get("pr_body", ""))

    # Missing Tests & Generation Button
    missing = data.get("missing_tests", [])
    if missing:
        st.subheader("⚠️ Test Gaps Detected")
        for gap in missing:
            st.warning(f"• {gap}")
            
        if st.button("🧪 Generate PyTest Stubs", use_container_width=True):
            with st.spinner("Generating automated test stubs..."):
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.groq.com/openai/v1"
                )
                stub_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a QA automation engineer. Generate clean pytest code for missing tests."},
                        {"role": "user", "content": f"Code:\n{code_input}\n\nGaps:\n{missing}"}
                    ]
                )
                st.session_state.test_stubs = stub_response.choices[0].message.content
                
    if st.session_state.test_stubs:
        st.subheader("🧪 Generated Test Stubs")
        st.code(st.session_state.test_stubs, language="python")
