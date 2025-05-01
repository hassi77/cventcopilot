import streamlit as st
from openai import OpenAI

# --- Page setup ---
st.set_page_config(page_title="📬 Hassanin's Sourcing Copilot", layout="centered")
st.image("cvent_logo.jpg", width=180)
st.title("📬 Hassanin's Sourcing Copilot")
st.caption("Ultra-personalized emails for third-party planners — powered by the Cvent Supplier Network.")

# --- OpenAI client ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- Research Inputs with toggle ---
st.markdown("### 🔍 Research Sources")

zi_unknown = st.checkbox("🔘 ZoomInfo not available")
zi_text = st.text_area("🧠 ZoomInfo", value="Unknown" if zi_unknown else "", height=150, disabled=zi_unknown)

li_unknown = st.checkbox("🔘 LinkedIn not available")
li_text = st.text_area("🔗 LinkedIn", value="Unknown" if li_unknown else "", height=150, disabled=li_unknown)

web_unknown = st.checkbox("🔘 Website not available")
web_text = st.text_area("🌐 Website / About Us", value="Unknown" if web_unknown else "", height=200, disabled=web_unknown)

# Combine research
site_text = f"ZoomInfo:\n{zi_text}\n\nLinkedIn:\n{li_text}\n\nWebsite:\n{web_text}"

# --- Prospect Details ---
st.markdown("### 👤 Prospect Details")
role = st.selectbox("Prospect Role", ["Managing Director", "Event Manager", "Project Manager", "Partner"])
agency_type = st.selectbox("Agency Type", ["DMC", "Venue Finder", "Event Agency", "PCO", "Travel Agency", "Mixed"])
event_types = st.multiselect("Event Types", ["Pharma", "Incentive", "Internal", "Corporate", "Brand Activation"])
events_per_year = st.slider("Estimated Events Per Year", 5, 100, 20)
pain_point = st.text_input("Biggest Pain Point (e.g. clients want something new)")

# --- Email Config ---
st.markdown("### 🛠 Email Config")
email_type = st.radio("Email Type", ["First-Hit", "Third-Hit"])
cta_style = st.selectbox("CTA Style", [
    "Worth a look?",
    "Want a quick example?",
    "Shall I send over a sample?",
    "Think it’s worth exploring?"
])

# --- Load the system prompt ---
with open("Full_Cvent_Sourcing_Copilot_System_Prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# --- Generate Email ---
if st.button("💡 Generate Email"):
    user_prompt = f"""Research provided:
{site_text}

Role: {role}
Agency Type: {agency_type}
Country: Unknown
Events per year: {events_per_year}
Event types: {', '.join(event_types)}
Biggest pain point: {pain_point}
Email Type: {email_type}
Preferred CTA: {cta_style}
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

        email_text = response.choices[0].message.content

        # --- Display result and copy ---
        st.markdown("### ✉️ Cold Email Output")
        st.text_area("📋 Your Cold Email (copy below)", value=email_text, height=250)
        st.caption("⬆️ Select + copy manually. CTA was: " + cta_style)
