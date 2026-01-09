from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from .data_utils import load_recipes
from .recipe_search import RecipeSearcher
from .model_wrapper import llm

app = FastAPI(title="Recipe Chatbot — Local")

recipes = load_recipes()
searcher = RecipeSearcher(recipes)

class IngredientsQuery(BaseModel):
    ingredients: List[str]
    top_k: int = 5

@app.get("/")
def root():
    return {"message": "Recipe Chatbot API. Use /recipes/search"}

@app.post("/recipes/search")
def recipe_search(q: IngredientsQuery):
    hits = searcher.find_by_ingredients(q.ingredients, top_k=q.top_k)
    if hits and hits[0]['overlap'] > 0:
        results = []
        for h in hits:
            rewrite = None
            if llm.model is not None:
                prompt = f"Rephrase this recipe conversationally:\nTitle: {h['title']}\nIngredients: {', '.join(h['ingredients'])}\nInstructions: {h['instructions']}"
                rewrite = llm.generate(prompt, max_tokens=200)
            results.append({**h, 'llm_rewrite': rewrite})
        return {"source": "retrieval", "results": results}
    # fallback
    if llm.model is not None:
        prompt = f"Create a simple recipe using these ingredients: {', '.join(q.ingredients)}. Provide title, ingredients, and step-by-step instructions."
        generated = llm.generate(prompt, max_tokens=300)
        return {"source": "llm", "generated": generated}
    return {"source": "fallback", "results": hits}
