from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import re
from typing import List
from .data_utils import load_recipes

def normalize_text(s: str):
    return re.findall(r"[a-zA-Z0-9_]+", s.lower())

class RecipeSearcher:
    def __init__(self, recipes: List[dict] = None):
        if recipes is None:
            recipes = load_recipes()

        # DEBUG: Print loaded recipes
        print("\n=== DEBUG: Loaded Recipes ===")
        print(recipes)
        print("Total recipes:", len(recipes))

        self.df = pd.DataFrame(recipes)

        # DEBUG: Print dataframe initial state
        print("\n=== DEBUG: DataFrame Created ===")
        print(self.df)

        # Build search text
        self.df['search_text'] = (
            self.df['title'].fillna('') + ' ' +
            self.df['ingredients'].apply(lambda ings: ' '.join(ings))
        )

        # DEBUG: Print search_text
        print("\n=== DEBUG: search_text Column ===")
        print(self.df['search_text'])

        self.vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b\w+\b')

        # DEBUG: Print before TF-IDF
        print("\n=== DEBUG: TF-IDF Input ===")
        print(list(self.df['search_text']))

        # Fit TF-IDF
        self.tfidf = self.vectorizer.fit_transform(self.df['search_text'])

        print("\n=== TF-IDF Vocabulary Size ===")
        print(len(self.vectorizer.vocabulary_))

    def find_by_ingredients(self, ingredient_list: List[str], top_k: int = 5):
        tokens = []
        for ing in ingredient_list:
            tokens += normalize_text(ing)

        query = ' '.join(tokens)
        q_vec = self.vectorizer.transform([query])

        from sklearn.metrics.pairwise import cosine_similarity
        sim = cosine_similarity(q_vec, self.tfidf).flatten()

        def overlap_score(row):
            recipe_tokens = []
            for ing in row['ingredients']:
                recipe_tokens += normalize_text(ing)
            return len(set(tokens).intersection(set(recipe_tokens)))

        self.df['overlap'] = self.df.apply(overlap_score, axis=1)
        res_df = self.df.copy()
        res_df['sim'] = sim
        res_df = res_df.sort_values(by=['overlap', 'sim'], ascending=False)
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
