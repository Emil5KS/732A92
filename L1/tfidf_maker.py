import sklearn as sk
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from proc_functions import process
import json


with open('proc_app_desc.json', 'r') as myfile:
    data = json.load(myfile)

descriptions = data.values()
app_names = list(data.keys())

#print(app_names)
# Det här är ett objekt
tf_app = TfidfVectorizer()

tf_matrix = tf_app.fit_transform(descriptions)


query = "Google mobile surfer"
query = [process(query)]

query = tf_app.transform(query)

search_result = cosine_similarity(tf_matrix, query)

k = 10
index = np.argsort(search_result, axis = 0 )[::-1][:k].flatten()

our_recomendations = [app_names[i] for i in index ]
print(our_recomendations)
