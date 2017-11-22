#import tm2
import spacy

def read_data(dir,n):
    with open(dir,"r") as file:
        for i,line in enumerate(file):
            if i < n:
                yield line
            else:
                break


data_file = "../data/gmb.txt"

#nlp = spacy.load('en', disable=['textcat'])

for sentence in read_data(data_file, n=3):
            print(sentence)


# nlp.pipe = parsing the text throuhg functions as tokenize and such.
# Enumerate makes a itterable thingy that makes each item a numberd sequence
#for i, doc in enumerate(nlp.pipe(read_data(data_file, n=5))):
#            for ent in doc.ents:
#                print("{}\t{}\t{}\t{}".format(ent.text, ent.start, ent.end, ent.label_))
