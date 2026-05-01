from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from .data_utils import load_recipes
from .recipe_search import RecipeSearcher
from .model_wrapper import llm
from .substitution import SUBSTITUTIONS

app = FastAPI(title="ChefMind — Offline AI Recipe Assistant")

recipes = load_recipes()
searcher = RecipeSearcher(recipes)

class IngredientsQuery(BaseModel):
    ingredients: List[str]
    top_k: int = 5

@app.get("/")
def root():
    return {"message": "ChefMind API running. Use /recipes/search"}

@app.post("/recipes/search")
def recipe_search(q: IngredientsQuery):

    # Clean input
    ingredients = [i.strip().lower() for i in q.ingredients if i.strip()]

    # Substitution suggestions
    substitutions = {
        ing: SUBSTITUTIONS[ing]
        for ing in ingredients if ing in SUBSTITUTIONS
    }

    hits = searcher.find_by_ingredients(ingredients, top_k=q.top_k)

    if hits and hits[0]['overlap'] > 0:
        results = []

        for h in hits:
            rewrite = None

            if llm.model is not None:
                prompt = f"""
Rewrite this recipe clearly and naturally.

Title: {h['title']}
Ingredients: {', '.join(h['ingredients'])}
Instructions: {h['instructions']}

Format:
- Title
- Ingredients (bullet points)
- Steps (numbered)
"""
                rewrite = llm.generate(prompt, max_tokens=200)

            results.append({**h, "llm_rewrite": rewrite})

        return {
            "source": "retrieval",
            "results": results,
            "substitutions": substitutions
        }

    # LLM fallback
    if llm.model is not None:
        prompt = f"""
Create a simple recipe using these ingredients:
{', '.join(ingredients)}

Provide:
- Title
- Ingredients
- Step-by-step instructions
"""
        generated = llm.generate(prompt, max_tokens=300)

        return {
            "source": "llm",
            "generated": generated,
            "substitutions": substitutions
        }

    return {
        "source": "fallback",
        "results": hits,
        "substitutions": substitutions
    }