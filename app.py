import streamlit as st
import requests

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Brand Voice AI",
    page_icon="🧠",
    layout="centered"
)

st.title("Brand Voice AI")
st.caption("Generate brand-consistent marketing copy instantly")

# -------------------------
# Preset Prompt Buttons
# -------------------------
st.subheader("Quick Presets")

col1, col2, col3 = st.columns(3)

if col1.button("Instagram Caption"):
    st.session_state.prompt_type = "Instagram caption"

if col2.button("Product Description"):
    st.session_state.prompt_type = "Product description"

if col3.button("Ad Copy"):
    st.session_state.prompt_type = "Ad copy"

prompt_type = st.session_state.get("prompt_type", "")

# -------------------------
# Input Section
# -------------------------
st.divider()
st.subheader("Input Details")

brand_name = st.text_input("Brand Name", placeholder="Nike")
product_name = st.text_input("Product Name", placeholder="Air Zoom Sneakers")

tone = st.selectbox(
    "Brand Tone",
    ["Luxury", "Casual", "Professional", "Friendly", "Bold", "Tech"]
)

custom_request = st.text_area(
    "Additional Instructions (optional)",
    placeholder="Target young audience, energetic style"
)

# -------------------------
# Generate Prompt
# -------------------------
def build_prompt():
    return f"""
Write a {prompt_type} for the brand "{brand_name}" and product "{product_name}".
Tone: {tone}.
{custom_request}
"""

# -------------------------
# AI Call
# -------------------------
def generate_response(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "arcee-ai/trinity-mini:free",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional brand copywriter."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# -------------------------
# Buttons
# -------------------------
st.divider()

colA, colB = st.columns(2)

generate = colA.button("Generate")
regenerate = colB.button("Regenerate")

# -------------------------
# Output
# -------------------------
if "result" not in st.session_state:
    st.session_state.result = ""

if generate or regenerate:
    if brand_name and product_name and prompt_type:
        with st.spinner("Generating response..."):
            final_prompt = build_prompt()
            st.session_state.result = generate_response(final_prompt)
    else:
        st.warning("Please fill Brand Name, Product Name and select a preset.")

if st.session_state.result:
    st.subheader("Generated Copy")
    st.text_area(
        "",
        st.session_state.result,
        height=300
    )
