import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

def token(text):
    return nltk.word_tokenize(text)

def rem_nonalphanum(words):
    #for word in words: using a list comprehension, the last for word in words removes this loop.
    return [ ''.join(ch for ch in word if ch.isalnum()) for word in words]

def lowercase(words):
    return [word.lower() for word in words]

def rm_stopwords(words):
    stop = set(stopwords.words('english'))
    return [word for word in words if word not in stop]

def stem(words):
    stemmer  = SnowballStemmer("english")
    return [stemmer.stem(word) for word in words]

def joiner(words):
    return ' '.join(words)

def process(text):
    function_list =[token,rem_nonalphanum,lowercase,rm_stopwords,stem,joiner]

    for function in function_list:
        text = function(text)
    return text
