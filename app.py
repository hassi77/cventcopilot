import streamlit as st
import openai

# Set up the Streamlit page
st.set_page_config(page_title="Hassanin's Sourcing Copilot", layout="centered")
st.title("📬 Hassanin's Sourcing Copilot")
st.caption("Generate high-converting Cvent outreach from TPP research in under 2 minutes.")

# OpenAI API Key
openai.api_key = st.secrets.get("OPENAI_API_KEY", "sk-...")

# ----------------------------
# Prospect Inputs
# ----------------------------
site_text = st.text_area("📝 Paste Website, LinkedIn, or ZoomInfo Info", height=250)
role = st.selectbox("👤 Prospect Role", ["Managing Director", "Event Manager", "Project Manager", "Partner"])
agency_type = st.selectbox("🏢 Agency Type", ["DMC", "Venue Finder", "Event Agency", "PCO", "Travel Agency", "Mixed"])
event_types = st.multiselect("🎯 Event Types", ["Pharma", "Incentive", "Internal", "Corporate", "Brand Activation"])
events_per_year = st.slider("📆 Events Per Year", 5, 100, 20)
pain_point = st.text_input("😣 Biggest Sourcing Pain Point (e.g. uses Excel, clients want something new)")
collab = st.text_input("🤝 Collaboration Style (e.g. internal team + venue finder)")
email_type = st.radio("✉️ Email Type", ["First-Hit", "Third-Hit"])
submit = st.button("💡 Generate Email")

# ----------------------------
# Load system prompt from external file
# ----------------------------
with open("Full_Cvent_Sourcing_Copilot_System_Prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# ----------------------------
# Run email generation
# ----------------------------
if submit and site_text:
    user_prompt = f"""
Website or LinkedIn info:
{site_text}

Role: {role}
Agency Type: {agency_type}
Country: Unknown
Events per year: {events_per_year}
Event types: {', '.join(event_types)}
Biggest pain point: {pain_point}
Collaboration: {collab}
Email Type: {email_type}
"""

    with st.spinner("Creating your outreach..."):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        st.markdown("### ✉️ Cold Email Output")
        st.success(response.choices[0].message.content)


