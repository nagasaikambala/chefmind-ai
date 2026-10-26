import streamlit as st
import requests
import time
import base64
import os

API_URL = "https://chefmind-ai-1.onrender.com/recipes/search"

# ================= CONFIG =================
st.set_page_config(page_title="ChefMind", page_icon="🍳", layout="wide")

# ================= BACKGROUND =================
def set_background():
    BASE_DIR = os.path.dirname(__file__)
    image_path = os.path.join(BASE_DIR, "assets", "bg.jpg")

    if not os.path.exists(image_path):
        st.error(f"❌ Image not found: {image_path}")
        return

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>

    /* 🔥 CORRECT TARGET */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
                    url("data:image/jpeg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Remove top white bar */
    [data-testid="stHeader"] {{
        background: transparent;
    }}

    </style>
    """, unsafe_allow_html=True)

# APPLY BACKGROUND
set_background()

# ================= GLOBAL CSS =================
st.markdown("""
<style>

/* Remove white blocks */
html, body, .block-container {
    background: transparent !important;
    color: white !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0.75) !important;
    color: white !important;
}

/* Chat messages */
.stChatMessage {
    background: rgba(0, 0, 0, 0.65) !important;
    color: white !important;
    border-radius: 15px;
    padding: 12px;
    backdrop-filter: blur(6px);
}

/* Input box */
[data-testid="stChatInput"] {
    background: rgba(0, 0, 0, 0.85) !important;
    border-radius: 12px !important;
}

/* Input text */
[data-testid="stChatInput"] textarea {
    color: white !important;
}

/* Placeholder */
textarea::placeholder {
    color: #cccccc !important;
}

/* Remove white input container */
.stChatInputContainer {
    background: transparent !important;
}

/* Remove leftover white blocks */
[data-testid="stVerticalBlock"] {
    background: transparent !important;
}

/* Text */
h1, h2, h3, h4, h5, h6, p, span, div, label {
    color: white !important;
}

button {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.title("⚙️ Settings")
top_k = st.sidebar.slider("Number of recipes", 1, 10, 5)

st.sidebar.markdown("---")
st.sidebar.info("💡 Tip: Try 'egg, onion, tomato'")

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []

# ================= TITLE =================
st.title("🍳 ChefMind")
st.caption("AI-powered offline cooking assistant")

# ================= CHAT =================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Enter ingredients (e.g., egg, onion)")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    ingredients = [i.strip().lower() for i in user_input.split(",") if i.strip()]

    payload = {
        "ingredients": ingredients,
        "top_k": top_k
    }

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        ```python
        try:
            with st.spinner("Cooking something delicious... 🍳"):
                # Allow extra time for Render's free service to wake up
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=(10, 90)
                )

                # Show HTTP errors instead of silently hiding them
                response.raise_for_status()
                data = response.json()

            time.sleep(0.5)

            reply = ""
            source = data.get("source")

            if source == "retrieval":
                reply += "### 🥘 Suggested Recipes\n\n"

                for r in data.get("results", []):
                    reply += f"#### 🍽️ {r.get('title', 'Untitled Recipe')}\n"
                    reply += (
                        f"**Ingredients:** "
                        f"{', '.join(r.get('ingredients', []))}\n\n"
                    )
                    reply += (
                        f"**Instructions:** "
                        f"{r.get('instructions', 'No instructions available.')}\n\n"
                    )
                    reply += "---\n"

                if not data.get("results"):
                    reply = "⚠️ No matching recipes were returned."

            elif source == "llm":
                reply += "### 🤖 AI Generated Recipe\n\n"
                reply += data.get("generated", "No generated recipe was returned.")

            else:
                reply = "⚠️ No strong matches found."

            message_placeholder.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        except requests.exceptions.Timeout:
            error_msg = (
                "⏳ ChefMind is taking longer than expected. "
                "The server may be waking up after inactivity. "
                "Please wait a little and try again."
            )
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })

        except requests.exceptions.HTTPError as e:
            status_code = response.status_code
            error_msg = (
                f"⚠️ The ChefMind backend returned HTTP {status_code}. "
                "Please try again shortly."
            )
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })

        except requests.exceptions.ConnectionError:
            error_msg = (
                "❌ Could not connect to the ChefMind backend. "
                "Please check the server and try again."
            )
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })

        except (ValueError, KeyError, TypeError):
            error_msg = (
                "⚠️ The backend returned an unexpected response. "
                "Please try again."
            )
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })

        except requests.exceptions.RequestException:
            error_msg = (
                "❌ A network error occurred while contacting ChefMind. "
                "Please try again."
            )
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })
```
