# 🍳 ChefMind — AI Recipe Assistant

ChefMind is an AI-powered recipe assistant that suggests recipes based on available ingredients. It combines classical NLP techniques with an interactive chatbot interface and is fully deployed online.

---

## 🌐 Live Demo

👉 https://chefmind-ai-3p26dkeln4uvd2kpvnvkaw.streamlit.app/

---

## 📌 Project Overview

ChefMind helps users decide what to cook using ingredients they already have.

- Enter ingredients like: `egg, onion`
- Get relevant recipes instantly
- Works as an interactive chatbot

---

## 🧠 Features

- 🔍 Ingredient-based recipe search
- ⚡ TF-IDF + cosine similarity for intelligent matching
- 🤖 Optional LLM-based recipe generation
- 💬 Chatbot-style UI (Streamlit)
- 🔄 Ingredient substitution suggestions
- 🌐 Fully deployed (Frontend + Backend)

---

## 🏗️ Tech Stack

**Frontend**
- Streamlit

**Backend**
- FastAPI

**Machine Learning**
- Scikit-learn (TF-IDF, cosine similarity)

**Other Tools**
- Pandas
- NumPy
- Requests

---

## ⚙️ Architecture

User Input → Streamlit UI → FastAPI Backend → TF-IDF Retrieval → Response → UI Display

---

## 🚀 Deployment

- Frontend deployed on **Streamlit Cloud**
- Backend deployed on **Render**

---

## 📁 Project Structure
chefmind-ai/
│
├── app/
│ ├── main.py
│ ├── recipe_search.py
│ ├── data_utils.py
│ ├── model_wrapper.py
│
├── ui/
│ ├── streamlit_app.py
│ └── assets/
│ └── bg.jpg
│
├── recipes.json
├── requirements.txt
├── runtime.txt
└── README.md


---

## 🧪 How It Works

1. User enters ingredients
2. Text is processed and normalized
3. TF-IDF vectorization is applied
4. Cosine similarity finds best matching recipes
5. Results are ranked and displayed
6. Optional LLM generates fallback recipe

---

## ▶️ Run Locally

```bash
# Clone repo
git clone https://github.com/nagasaiKambala/chefmind-ai.git

# Go to folder
cd chefmind-ai

# Create virtual env
python -m venv .venv

# Activate
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload

# Run frontend (new terminal)
streamlit run ui/streamlit_app.py

<img width="1918" height="906" alt="image" src="https://github.com/user-attachments/assets/1bc47778-9d74-4527-bed9-4e0b6bfecabc" />


💼 Resume Description

Built and deployed ChefMind, an AI-powered recipe assistant using FastAPI and Streamlit, leveraging TF-IDF and cosine similarity for ingredient-based retrieval, with optional LLM integration and full-stack deployment.

🔮 Future Improvements
🎤 Voice input for ingredients
📸 Image-based ingredient detection
❤️ Save favorite recipes
🌍 Multi-language support
🤖 Advanced LLM integration

🙌 Acknowledgements
Open-source ML libraries
Streamlit & FastAPI communities

📧 Contact

NagaSai
📍 Hyderabad, India
💼 AI/ML Engineer
