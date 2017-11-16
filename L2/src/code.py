import spacy
import re

def read_data(data_file, n=None):
    with open(data_file, "r") as infile:
        for i, line in enumerate(infile):
            if n is None or i < n:
                yield line
            else:
                break

data_file = "../data/gmb.txt"
gold_file = "../data/gold.txt"

data = read_data(data_file)
gold_data = read_data(gold_file)

nlp = spacy.load("en", disable=["textcat"])

# for sentence in read_data(data_file, n=3):
#     print(sentence)

# for i, doc in enumerate(nlp.pipe(read_data(data_file, 3))):
#     for ent in doc.ents:
#         print("{}\t{}\t{}\t{}".format(ent.text, ent.start, ent.end, ent.label_))

# for i, doc in enumerate(nlp.pipe(test)):
#     for ent in doc.ents:
#         print("{}\t{}\t{}\t{}".format(ent.text, ent.start, ent.end, ent.label_))

def extract(doc):
    """
    Extract relevant relation instances from the specified document.

    Args:
        doc: The sentence as analysed by spaCy.

    Yields:
        Pairs of strings representing the extracted relation instances.
    """
    # pattern = re.compile(r'.*\b(head|lead|boss|manag|command|direct|rul)\b(?!\b.+ing).*')
    pattern = re.compile(r'.*(head|lead|boss|manag|command|direct|rul).*')

    person_start = None
    person_end = None
    org_start = None
    org_end = None

    pairs = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            person_label = ent.text
            person_start = ent.start
            person_end = ent.end
        elif person_start is not None and ent.label_ == "ORG":
            org_label = ent.text
            org_start = ent.start
            org_end = ent.end

        if person_start is not None and org_end is not None:
            words = doc.text.split()
            relation = " ".join(words[person_end:org_start]).strip()

            if pattern.match(relation):
                person = person_label.strip()
                organization = org_label.strip()

                if person and organization:
                    pairs.append((person, organization))

            person_start = None
            person_end = None
            org_start = None
            org_end = None

    return pairs

extracted = set()

for i, doc in enumerate(nlp.pipe(data)):
    entities = extract(doc)

    for person, org in entities:
        extracted.add((i, person, org))

gold = set()

for line in gold_data:
    columns = line.rstrip().split('\t')
    gold.add((int(columns[0]), columns[1], columns[2]))

def evaluate(reference, predicted):
    """
    Print out the precision, recall, and F1 for the id-entity-entity
    triples in the set `predicted`, given the triples in the reference set.
    Args:
        reference: The reference set of triples.
        predicted: The set of predicted triples.
    """
    true_positive = len(predicted.intersection(reference))
    false_negative = len(reference - predicted)
    false_positive = len(predicted - reference)

    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    f1 = 2 * precision * recall / (precision + recall)

    return precision * 100, recall * 100, f1 * 100


print("Intersection Without Normalisation")
print(extracted.intersection(gold))
print(len(extracted.intersection(gold)))
evaluation = evaluate(gold, extracted)
print("Precision: %0.2f, Recall: %0.2f, F1-Score: %f0.2f" % evaluation)

def normalise(i, person, org):
    person_parts = {part.lower() for part in set(person.split())}

    for j, p, o in gold:
        if j == i:
            pparts = {part.lower() for part in set(p.split())}
            intersection = pparts.intersection(person_parts)

            if len(intersection) > 0:
                return j, p, o

    return i, person, org

extracted_normalised = set()

for element in extracted:
    extracted_normalised.add(normalise(*element))

print("Intersection With Normalisation")
print(extracted_normalised.intersection(gold))
print(len(extracted_normalised.intersection(gold)))
evaluation_normalised = evaluate(gold, extracted_normalised)
print("Precision: %0.2f, Recall: %0.2f, F1-Score: %f0.2f" % evaluation_normalised)


with open("../data/extracted.txt", "w") as outfile:
    for i, p, o in extracted:
        outfile.write("%i\t%s\t%s\n" % (i, p, o))
