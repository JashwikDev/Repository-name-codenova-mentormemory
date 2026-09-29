import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

load_dotenv(override=True)

# -------------------------
# API CLIENTS
# -------------------------

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

hindsight_client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

# One memory bank for our demo student
BANK_ID = "codenova-mentormemory-jashwik"

# -------------------------
# UI
# -------------------------

st.title("MentorMemory AI")
st.caption("An AI tutor that learns and remembers the student.")

user_input = st.text_input(
    "Ask your tutor something"
)

if st.button("Send") and user_input:

    # -------------------------
    # -------------------------
# 1. RECALL RELEVANT MEMORY
# -------------------------

memories = []
memory_context = ""

try:
    memory_result = hindsight_client.recall(
        bank_id=BANK_ID,
        query=user_input,
        max_tokens=800,
        budget="low"
    )

    # Keep only the most relevant few memories for the demo
    for item in memory_result.results[:5]:
        memories.append(item.text)

    memory_context = "\n".join(memories)

    if memories:
        with st.expander("🧠 What MentorMemory remembered", expanded=True):
            for memory in memories:
                st.write("•", memory)
    else:
        st.info("No relevant memories found yet.")

except Exception as e:
    st.warning(f"Memory recall issue: {e}")