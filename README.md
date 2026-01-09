📘 README — Task 2: Local LLM Integration & Recipe Chatbot
📌 Project Overview

This project implements a local recipe chatbot system using:

Python 3.11.9 (Required)

FastAPI → Backend API

TF-IDF + Cosine Similarity → Ingredient-based recipe retrieval

Optional Local LLM Support → Generates recipes when no match is found

Streamlit UI → Chatbot-style user interface

Users can enter ingredients (e.g., "egg, onion") and receive relevant recipes.

The entire project runs offline on any Windows/Linux machine.

📁 Project Structure
Bookxpert_Task2/
│
├── app/
│   ├── main.py               # FastAPI server
│   ├── recipe_search.py      # TF-IDF search logic
│   ├── data_utils.py         # Loads recipes.json
│   ├── model_wrapper.py      # Optional local LLM wrapper
│
├── ui/
│   └── streamlit_app.py      # Chatbot UI
│
├── recipes.json               # 50-recipe dataset
├── requirements.txt
├── README.md


⚠️ Note: Virtual environment (.venv/) should NOT be included in ZIP.

⚙️ 1. Setup Instructions
🐍 Python Version Requirement

This project must be run with:

Python 3.11.9


Older Python (3.7, 3.10) or newer (3.13) will fail to install scikit-learn and urllib3.

✔️ Step 1 — Create Virtual Environment
py -3.11 -m venv .venv

✔️ Step 2 — Activate Virtual Environment

Windows PowerShell:

.\.venv\Scripts\activate


Linux/macOS:

source .venv/bin/activate


You should now see:

(.venv)

✔️ Step 3 — Install Dependencies
pip install -r requirements.txt

🚀 2. Run FastAPI Backend

Start the backend API:

uvicorn app.main:app --reload --port 8000


Backend will run at:

http://127.0.0.1:8000

Test the server

Visit:

http://127.0.0.1:8000/


Expected:

{"message": "Recipe Chatbot API. Use /recipes/search"}

🥘 3. API Usage
Endpoint
POST /recipes/search

Sample Request (curl)
curl -X POST http://127.0.0.1:8000/recipes/search ^
-H "Content-Type: application/json" ^
-d "{\"ingredients\": [\"egg\", \"onion\"], \"top_k\": 5}"

Sample Response
{
  "source": "retrieval",
  "results": [
    {
      "title": "Egg Onion Omelette",
      "ingredients": ["egg", "onion", "salt", "pepper", "oil"],
      "instructions": "Beat eggs with onions and spices, then cook in oil.",
      "overlap": 2,
      "similarity": 0.78,
      "llm_rewrite": null
    }
  ]
}


If no recipe matches ingredients:

source: "llm"


(Only if LLM enabled; otherwise falls back to retrieval.)

💬 4. Run Streamlit Chatbot UI

Open a new terminal → activate venv:

.\.venv\Scripts\activate


Run UI:

streamlit run ui/streamlit_app.py


App opens at:

http://localhost:8501


Enter ingredients (example):

egg, onion


Output:

Egg Onion Omelette

Tomato Egg Curry

Egg Fried Rice (if ingredients overlap)

🗃️ 5. Dataset — recipes.json

Includes 50 recipes (veg + non-veg):

Breakfast (Upma, Idli, Dosa, Pancakes)

Lunch/Dinner (Biryani, Paneer Butter Masala, Sambar)

Snacks (Veg Sandwich, French Toast)

Indian, Chinese, Italian Inspired

Egg, Veg, Chicken, Fish, Paneer dishes

The larger dataset improves TF-IDF retrieval accuracy.

🤖 6. Local LLM Integration (Optional)

You may load a local model (GPT4All, Llama.cpp) in:

app/model_wrapper.py


Default:

llm.model = None


This disables LLM generation and uses retrieval-only mode.

Project runs fine without any LLM installed.

⚙️ 7. How to Run the Entire Project (Quick Guide)
1. Install Python 3.11.9
2. py -3.11 -m venv .venv
3. Activate venv
4. pip install -r requirements.txt
5. uvicorn app.main:app --reload --port 8000
6. streamlit run ui/streamlit_app.py


Everything runs locally and offline.

📦 8. Requirements

From requirements.txt:

fastapi==0.95.2
uvicorn==0.22.0
pandas==2.2.3
scikit-learn==1.3.2
streamlit
pydantic
requests


Tested with Python 3.11.9.