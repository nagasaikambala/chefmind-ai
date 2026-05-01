from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re
from typing import List
from .data_utils import load_recipes

def normalize_text(s: str):
    words = re.findall(r"[a-zA-Z0-9_]+", s.lower())
    return [w.rstrip('s') for w in words]  # simple normalization

class RecipeSearcher:
    def __init__(self, recipes: List[dict] = None):
        if recipes is None:
            recipes = load_recipes()

        self.df = pd.DataFrame(recipes)

        # Create search text
        self.df['search_text'] = (
            self.df['title'].fillna('') + ' ' +
            self.df['ingredients'].apply(lambda ings: ' '.join(ings))
        )

        # Precompute ingredient tokens (IMPORTANT optimization)
        self.df['ingredient_tokens'] = self.df['ingredients'].apply(
            lambda ings: set(sum([normalize_text(i) for i in ings], []))
        )

        # TF-IDF
        self.vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b\w+\b')
        self.tfidf = self.vectorizer.fit_transform(self.df['search_text'])

    def find_by_ingredients(self, ingredient_list: List[str], top_k: int = 5):
        tokens = []
        for ing in ingredient_list:
            tokens += normalize_text(ing)

        query = ' '.join(tokens)
        q_vec = self.vectorizer.transform([query])

        from sklearn.metrics.pairwise import cosine_similarity
        sim = cosine_similarity(q_vec, self.tfidf).flatten()

        # Compute overlap efficiently
        self.df['overlap'] = self.df['ingredient_tokens'].apply(
            lambda recipe_tokens: len(set(tokens).intersection(recipe_tokens))
        )

        res_df = self.df.copy()
        res_df['sim'] = sim

        # ⭐ Weighted scoring (IMPORTANT)
        res_df['final_score'] = 0.7 * res_df['overlap'] + 0.3 * res_df['sim']

        res_df = res_df.sort_values(by='final_score', ascending=False)

        filtered = res_df[res_df['overlap'] > 0]
        if filtered.empty:
            filtered = res_df

        out = []
        for _, row in filtered.head(top_k).iterrows():
            out.append({
                'title': row['title'],
                'ingredients': row['ingredients'],
                'instructions': row.get('instructions', ''),
                'overlap': int(row['overlap']),
                'similarity': float(row['sim'])
            })

        return out