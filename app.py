import streamlit as st
from openai import OpenAI
import datetime
import csv
import os

# Set your OpenAI API key
import streamlit as st
OPENAI_API_KEY = st.secrets["openai_api_key"]  # ✅ Secure
client = OpenAI(api_key=OPENAI_API_KEY)


# Streamlit setup
st.set_page_config(page_title="Cvent Email Copilot", layout="wide")
st.title("📧 Cvent Email Copilot")
st.caption("Generate CSN-branded outbound emails based on role and event type")
st.markdown("""
<style>
    .stButton>button { background-color: #00338d; color: white; border-radius: 8px; font-weight: 600; }
    .stTextArea textarea, .stTextInput input { border-radius: 8px; }
    .reportview-container .main .block-container{ padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# Layout: Full width form
st.subheader("🔍 Paste Research")

linkedin_disabled = st.checkbox("❌ No LinkedIn Info")
linkedin_info = st.text_area("LinkedIn Bio (optional)", height=100, disabled=linkedin_disabled)

zoominfo_disabled = st.checkbox("❌ No ZoomInfo Info")
zoominfo_info = st.text_area("ZoomInfo / Copilot Info (optional)", height=100, disabled=zoominfo_disabled)

website_disabled = st.checkbox("❌ No Website Info")
website_info = st.text_area("Website Description (optional)", height=100, disabled=website_disabled)

role = st.selectbox("🧑 Prospect Role", ["Managing Director", "Event Manager", "Project Manager", "Partner"])
agency_type = st.selectbox("🏢 Agency Type", ["DMC", "Venue Finder", "Event Agency", "PCO", "Travel Agency", "Mixed"])
event_types = st.multiselect("🎯 Event Types", [
    "Pharma", "Incentive", "Internal", "Corporate", "Brand Activation",
    "Hybrid", "Congress", "Teambuilding", "Luxury", "Sports", "Wellness"
])

events_skipped = st.checkbox("❌ No Event Count Info")
events_per_year = st.slider("📆 Events Per Year", 5, 100, 20, disabled=events_skipped)

pain_point = st.text_input("💢 Biggest Pain Point")
email_type = st.radio("✉️ Email Type", ["First-Hit", "Third-Hit"])
tone = st.select_slider("🎤 Tone Preference", options=["Professional", "Balanced", "Conversational"])

submit = st.button("✨ Generate Email")
alternate = st.button("🔁 Try Different CTA")

if submit or alternate:
    system_prompt = """You are a highly trained AI sales assistant for Cvent, supporting outbound emails for the Cvent Supplier Network (CSN). Write cold outbound emails (under 125 words) to European third-party event agencies.\n\nRules:\n- Use ✅ to highlight 2–3 CSN value props\n- Skip small talk\n- End with a soft CTA like \"Worth a look?\" or \"Can I send over an example?\"\n- Match tone based on user's selection\n- If the prospect is a Managing Director or Partner, split the email into two parts:\n    1. Here's how you benefit: (3 bullets)\n    2. Here's how your team benefits: (3 bullets)\n- If it's a Project or Event Manager, focus on solving sourcing pain, streamlining proposals, and winning client trust\n\nRespond with only the email body.\n"""

    combined_input = f"""
LinkedIn Info:
{linkedin_info}

ZoomInfo Info:
{zoominfo_info}

Website Info:
{website_info}

Role: {role}
Agency Type: {agency_type}
Event Types: {', '.join(event_types)}
Events per year: {'' if events_skipped else events_per_year}
Pain Point: {pain_point}
Email Type: {email_type}
Tone: {tone}
CTA Style: {'alternate' if alternate else 'standard'}
"""

    with st.spinner("Generating email..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": combined_input}
                ],
                temperature=0.8,
                max_tokens=400
            )

            final_email = response.choices[0].message.content

            st.markdown("### ✉️ Generated Email")
            st.text_area("Copy or edit this email:", final_email, height=200)
            st.download_button("📋 Copy to Clipboard", final_email, file_name="email.txt")

        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")

