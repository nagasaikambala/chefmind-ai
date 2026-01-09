import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recipes/search"

st.title("🍳 Recipe Chatbot")
st.write("Enter ingredients separated by commas. Example: `egg, onion`")

user_input = st.text_input("Ingredients:")

if st.button("Get Recipe"):
    if user_input.strip() == "":
        st.warning("Please enter some ingredients.")
    else:
        ingredients = [i.strip() for i in user_input.split(",")]

        payload = {
            "ingredients": ingredients,
            "top_k": 5
        }

        try:
            response = requests.post(API_URL, json=payload)
            data = response.json()

            if data["source"] == "retrieval":
                st.subheader("🥘 Suggested Recipes")
                for r in data["results"]:
                    st.write(f"### {r['title']}")
                    st.write(f"**Ingredients:** {', '.join(r['ingredients'])}")
                    st.write(f"**Instructions:** {r['instructions']}")
                    st.write("---")

            elif data["source"] == "llm":
                st.subheader("🤖 AI-Generated Recipe")
                st.write(data["generated"])

        except Exception as e:
            st.error("API error: Could not reach the backend server.")
            st.error(str(e))
