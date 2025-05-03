import re
from nltk.corpus import wordnet
import nltk

nltk.download('wordnet', quiet=True)

def clean_ingredient_name(ingredient):
    ingredient = ingredient.lower()
    ingredient = re.sub(r'\([^)]*\)', '', ingredient)  
    ingredient = re.sub(r'[^a-zA-Z\s]', '', ingredient)  
    return ingredient.strip()

def get_synonym_from_wordnet(word):
    synsets = wordnet.synsets(word)
    if synsets:
        lemmas = synsets[0].lemmas()
        if lemmas:
            return lemmas[0].name().replace('_', ' ')
    return word

def normalize_ingredient_name(ingredient):
    cleaned = clean_ingredient_name(ingredient)
    tokens = cleaned.split()
    normalized_tokens = [get_synonym_from_wordnet(token) for token in tokens]
    return ' '.join(normalized_tokens)