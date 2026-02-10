import sys
import streamlit as st
import pandas as pd
from datetime import datetime
from google import genai
from google.genai import types

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="FarmaBuddy 🌱",
    page_icon="🌾",
    layout="wide"
)



# ---------------- API KEY & CLIENT ----------------
# We force the 'v1' stable API version to resolve the 404 issue.
# Change this in your CONFIG section
# In your API KEY & CLIENT section
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"],
)
# Add this temporary button to your sidebar to check names

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>🌱 FarmaBuddy</h1>
    <h4 style='text-align:center;'>AI-Powered Smart Farming Assistant</h4>
    <p style='text-align:center;'>Built using Gemini | Deployed with Streamlit</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- USER INPUTS ----------------
st.sidebar.header("🌍 Farmer Inputs")
region = st.sidebar.selectbox("Select Region", ["India", "Ghana", "Canada"])
location = st.sidebar.text_input("Enter Location (State / Province)")
crop_stage = st.sidebar.selectbox("Crop Stage", ["Planning", "Sowing", "Growing", "Harvesting"])
priority = st.sidebar.multiselect("Your Priorities", ["Low Water Use", "High Yield", "Organic Farming", "Low Cost"])
temperature = st.sidebar.slider("AI Creativity Level", 0.2, 0.9, 0.5)

# ---------------- PROMPT ENGINE ----------------
def build_prompt():
    return f"""
You are a highly experienced agricultural advisor with deep knowledge of
crop management, soil health, irrigation, pest control, and climate-based farming.

FARMER PROFILE:
- Region: {region}
- Location: {location}
- Crop Growth Stage: {crop_stage}
- Farmer Priorities: {', '.join(priority)}

OBJECTIVE:
Help the farmer improve yield, reduce risk, and manage resources efficiently.

TASK INSTRUCTIONS:
Provide EXACTLY 3 detailed farming recommendations tailored to the farmer profile.

FOR EACH RECOMMENDATION, YOU MUST:
1. Clearly state the action the farmer should take.
2. Explain WHY this action is important at the current crop stage.
3. Describe HOW it helps with the farmer’s stated priorities.
4. Mention any risk if the advice is ignored (if applicable).

FORMAT RULES (STRICT):
- Use numbered bullet points (1, 2, 3).
- Each recommendation must be at least 3–4 lines long.
- Do NOT combine recommendations.
- Keep language simple, practical, and farmer-friendly.
- Avoid scientific jargon.
- Use line breaks for readability.

OUTPUT FORMAT (FOLLOW EXACTLY):

1. Recommendation:
   - What to do:
   - Why it is useful:
   - How it helps the farmer:
   - Risk if ignored:

2. Recommendation:
   - What to do:
   - Why it is useful:
   - How it helps the farmer:
   - Risk if ignored:

3. Recommendation:
   - What to do:
   - Why it is useful:
   - How it helps the farmer:
   - Risk if ignored:
"""


# ---------------- MAIN ACTION ----------------
if st.button("🌾 Get Smart Advice"):
    if not location:
        st.warning("Please enter your location.")
    else:
        response = client.models.generate_content(
        model="gemini-3-flash-preview",                # <--- UPDATE THIS
        contents=build_prompt(),
        config={"temperature": temperature, "max_output_tokens": 512}
        )
        st.success("Here’s your AI-generated farming advice:")
        st.markdown(response.text)
 

# ---------------- FEEDBACK CHECKLIST ----------------
st.markdown("## ✅ AI Output Validation Checklist")
feedback = {
    "Region-specific advice": st.checkbox("Advice is specific to my region"),
    "Logical reasoning": st.checkbox("Suggestions include valid reasoning"),
    "Simple language": st.checkbox("Language is easy to understand"),
    "Actionable steps": st.checkbox("Advice can be applied practically"),
    "Safe & ethical": st.checkbox("No unsafe or misleading information")
}

if st.button("📊 Submit Feedback"):
    score = sum(feedback.values())
    st.info(f"Feedback Score: {score}/5")

# ---------------- USAGE LOG ----------------
st.markdown("## 📈 Usage Snapshot")
log_data = {"Time": datetime.now().strftime("%Y-%m-%d %H:%M"), "Region": region, "Crop Stage": crop_stage}
st.dataframe(pd.DataFrame([log_data]))

# ---------------- FOOTER ----------------
st.markdown("<hr><p style='text-align:center; font-size:14px;'>FA-2 Project | 2026</p>", unsafe_allow_html=True)
