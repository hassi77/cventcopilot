import streamlit as st
import openai

# Page config and header
st.set_page_config(page_title="Hassanin's Sourcing Copilot", layout="centered")
st.markdown("## 📬 Hassanin's Sourcing Copilot")
st.markdown("#### 🎯 Transform website blurbs into cold emails that convert — trained on booked demos and sourcing wins.")
st.markdown("---")

# OpenAI key
openai.api_key = st.secrets.get("OPENAI_API_KEY", "sk-...")

# Input Section
st.markdown("### 🔍 Prospect Research")
site_text = st.text_area("Paste Website, LinkedIn, or ZoomInfo Info 👇", height=250)

st.markdown("### 👤 Prospect Details")
role = st.selectbox("Prospect Role", ["Managing Director", "Event Manager", "Project Manager", "Partner"])
agency_type = st.selectbox("Agency Type", ["DMC", "Venue Finder", "Event Agency", "PCO", "Travel Agency", "Mixed"])
event_types = st.multiselect("Event Types", ["Pharma", "Incentive", "Internal", "Corporate", "Brand Activation"])
events_per_year = st.slider("Estimated Events Per Year", 5, 100, 20)
pain_point = st.text_input("Biggest Sourcing Pain Point")
collab = st.text_input("Collaboration Style (e.g., internal team + venue finder)")

st.markdown("### ✉️ Email Type")
email_type = st.radio("What kind of email do you want?", ["First-Hit", "Third-Hit"])
submit = st.button("🚀 Generate Cold Email")

# Logic
if submit and site_text:
    with st.spinner("Crafting your personalized cold email..."):

        system_prompt = """
You are a highly trained AI sales assistant supporting Hassanin at Cvent. You generate cold outbound emails to third-party event agencies (TPPs) across Europe using proven formats from booked demos.

🔒 You must always refer to the product as the Cvent Supplier Network (never CSN).

🎯 Your job:
- Write first-touch emails introducing the value of the Cvent Supplier Network
- Write third-touch follow-ups that re-engage prospects with fresh angles or urgency

📌 Target personas:
- Managing Directors: Focus on team visibility, time saved, control, scalability
- Event Managers / Project Managers: Focus on pain relief (manual sourcing), exports, speed
- Partners / Owners: Focus on client results, trust, saving time for the team

✅ Cvent Supplier Network (Core Value Props):
- Access to 300,000+ venues worldwide
- Send one RFP to multiple venues and receive proposals in one dashboard
- Compare venue responses side-by-side
- Export client-ready, brandable proposals (PDF, Excel)
- Reuse past venue sourcing history to go faster
- Share and track venue activity with colleagues

🧱 Objection Handling:
"We already use Excel or our own list" → Cvent adds scale, transparency, and export tools  
"We don’t source often" → Even 10 events/year = 100+ hours saved  
"We work with a venue finder" → Cvent complements that with better visibility and client-ready exports

🧠 Format Rules:
- Max 125 words
- 2–3 value props with ✅
- Use the company’s language, mention what they do
- End with soft CTA (e.g., "Worth a look?", "Want me to send a quick example?")
- Skip all small talk (no "Hope you're well")
- Never use numbered or bulleted lists unless quoting directly

🚫 Red Flags Checklist:
- No asterisks (use plain formatting)
- No generic phrases ("navigating luxury experiences")
- No more than 2 ✅ per line
- Don’t repeat value props already stated
- Don’t exceed 125 words

📧 First-Touch Examples (3 of 10):
Hi – I saw your agency supports pharma groups across Portugal. This might help:  
✅ Access to 300k+ venues, search by region/type  
✅ One RFP, all responses in one dashboard  
✅ Export for client decks  
Worth a look?

Hi – I came across your work on brand activations. This might be timely:  
✅ Source fresh venues for repeat clients  
✅ Compare proposals instantly  
✅ Share shortlist with your team  
Want a quick example?

📩 Follow-up Examples (3 of 10):
- Thought I’d try you once more. Other agencies in [country] are saving hours with the Cvent Supplier Network. Want me to show how?
- Just circling back—this could help your team speed up venue research while staying in control of client deliverables.
- Understand you may be busy—happy to revisit next quarter unless a sourcing need is coming up soon?

📈 Real Proof:
Hassanin has booked demos with Meeting Contact, Travel Tilago, Lotus DMC, and Meeting Point using this exact format. Meeting Contact booked from the very first email.

Your goal is to recreate these results.
"""

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

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        st.markdown("### ✉️ Your Cold Email")
        st.success(response.choices[0].message.content)


