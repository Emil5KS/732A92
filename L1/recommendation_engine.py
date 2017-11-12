import json
import sklearn as sk
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from proc_functions import tf_proces

with open('proc_app_desc.json', 'r', encoding="utf-8") as infile:
    data = json.load(infile)

descriptions = list(data.values())
app_names = list(data.keys())

vectorizer = TfidfVectorizer()
tfidf_desc_mat = vectorizer.fit_transform(descriptions)

def get_recommendations(query, n=10):
    tfidf_query_vec = vectorizer.transform([tf_process(query)])

    search_result = cosine_similarity(tfidf_query_vec, tfidf_desc_mat).flatten().tolist()
    index = np.argsort(search_result, axis = 0)[::-1][:n]
    recommendations = [app_names[i] for i in index]

    return recommendations


print(get_recommendations("photo image social"))
print(get_recommendations("game video fun"))
