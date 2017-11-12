import nltk

from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

def tf_tokenize(text):
    return nltk.word_tokenize(text)

def rm_nonalphanum(words):
    return [''.join(ch for ch in word if ch.isalnum()) for word in words]

def tf_lowercase(words):
    return [word.lower() for word in words]

def rm_stopwords(words):
    stops = set(stopwords.words('english'))
    return [word for word in words if word not in stops]

def tf_stem(words):
    stemmer  = SnowballStemmer("english")
    return [stemmer.stem(word) for word in words]

def tf_join(words):
    return ' '.join(words)

def tf_process(text):
    function_list =[tf_tokenize, rm_nonalphanum, tf_lowercase,
                    rm_stopwords, tf_stem, tf_join]

    for function in function_list:
        text = function(text)

    return text
