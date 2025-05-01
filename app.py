import streamlit as st
from openai import OpenAI

# Set page config
st.set_page_config(page_title="Hassanin's Sourcing Copilot", layout="centered")
st.title("📬 Hassanin's Sourcing Copilot")
st.caption("Generate high-converting Cvent outreach from TPP research in under 2 minutes.")

# Load OpenAI key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Prospect Research Input
st.markdown("### 🔍 Paste Any Research You Have")
zi_text = st.text_area("🧠 ZoomInfo (if available)", height=150)
li_text = st.text_area("🔗 LinkedIn (if available)", height=150)
web_text = st.text_area("🌐 Website / About Us", height=200)

# Combine research
site_text = f"ZoomInfo:\n{zi_text}\n\nLinkedIn:\n{li_text}\n\nWebsite:\n{web_text}"

# Role and context inputs
st.markdown("### 👤 Prospect Details")
role = st.selectbox("Prospect Role", ["Managing Director", "Event Manager", "Project Manager", "Partner"])
agency_type = st.selectbox("Agency Type", ["DMC", "Venue Finder", "Event Agency", "PCO", "Travel Agency", "Mixed"])
event_types = st.multiselect("Event Types", ["Pharma", "Incentive", "Internal", "Corporate", "Brand Activation"])
events_per_year = st.slider("Estimated Events Per Year", 5, 100, 20)
pain_point = st.text_input("Biggest Pain Point (e.g. uses Excel, clients want something new)")
email_type = st.radio("Email Type", ["First-Hit", "Third-Hit"])

# Button to handle unknown research
if st.button("🔍 I have no research — mark all Unknown"):
    zi_text = "Unknown"
    li_text = "Unknown"
    web_text = "Unknown"
    site_text = f"ZoomInfo:\n{zi_text}\n\nLinkedIn:\n{li_text}\n\nWebsite:\n{web_text}"
    st.success("Marked all research sources as Unknown.")

# Load the long system prompt from file
with open("Full_Cvent_Sourcing_Copilot_System_Prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# Generate Email Button
if st.button("💡 Generate Email") and site_text:
    user_prompt = f"""Research provided:
{site_text}

Role: {role}
Agency Type: {agency_type}
Country: Unknown
Events per year: {events_per_year}
Event types: {', '.join(event_types)}
Biggest pain point: {pain_point}
Email Type: {email_type}
"""

    with st.spinner("Generating your cold email..."):
        response = client.chat.completions.create(
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


