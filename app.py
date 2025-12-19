import streamlit as st
import requests

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="Brand Voice AI",
    page_icon="🧠",
    layout="centered"
)

# -------------------------
# Title
# -------------------------
st.title("Brand Voice AI")
st.caption("Generate brand-consistent marketing copy using AI")

# -------------------------
# User Input
# -------------------------
prompt = st.text_input(
    "Enter your request",
    placeholder="Write an Instagram caption for a tech product"
)

generate = st.button("Generate")

# -------------------------
# AI Function
# -------------------------
def generate_response(user_prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "arcee-ai/trinity-mini:free",
        "messages": [
            {"role": "system", "content": "You are a premium brand copywriter."},
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# -------------------------
# Output
# -------------------------
if generate and prompt:
    with st.spinner("Generating response..."):
        result = generate_response(prompt)
        st.text_area("Generated Copy", result, height=300)
