import numpy, random, scipy.special

import matplotlib.pyplot as plt

class MyGibbs(object):    
    def __init__(self,
                 num_topics,
                 docs_file_name,
                 stop_list_file_name = None):
        self.num_topics = num_topics
        self.num_docs = 0
        self.doc_snippets = []
        self.docs = []

        ## Prepare list of stopwords
        self.stoplist = dict()
        if stop_list_file_name != None:
            with open(stop_list_file_name) as f:
                for line in f:
                    word = line.rstrip()
                    self.stoplist[word] = 1
        
        self.read_documents(docs_file_name)
        self.initialize_matrices()
        
    def initialize_matrices(self):
        """Initializes numpy arrays for the matrix computations performed
        by the sampler during the MCMC process."""
        ## Set up numpy matrices
        self.term_topics = numpy.zeros((self.num_terms, self.num_topics))
        self.doc_topics = numpy.zeros((self.num_docs, self.num_topics))
        self.topic_totals = numpy.zeros(self.num_topics)
        self.doc_totals = numpy.zeros(self.num_docs)

        ## Initialize topics randomly
        for doc_id in range(self.num_docs):
            doc = self.docs[doc_id]
            ## Create an array of random topic assignments
            doc['topics'] = list(map(lambda x: random.randrange(self.num_topics), doc['tokens']))
            ## Construct the initial summary statistics
            doc_length = len(doc['tokens'])
            for i in range(doc_length):
                token = doc['tokens'][i]
                topic = doc['topics'][i]
                self.term_topics[token][topic] += 1 # n_wk
                self.doc_topics[doc_id][topic] += 1 # n_dk
                self.topic_totals[topic] += 1       # n_k
                self.doc_totals[doc_id] += 1

        ## Printout to check that everything is coherent
        # print(sum(sum(self.doc_topics)))
        # print(sum(sum(self.term_topics)))
        # print(sum(self.topic_totals))
        # print(sum(self.doc_totals))

    
    def read_documents(self, filename):
        """Reads documents from a file, filters stop words and initializes
        the vocabulary. Also converts tokens to integer term IDs."""
        self.vocab = []
        self.vocab_ids = {}

        with open(filename) as f:
            for line in f:
                line = line.replace(".", " ").replace(",", " ").lower()
                self.num_docs += 1
                tokens = []

                for w in line.split():
                    if not w in self.stoplist:
                        if w in self.vocab_ids:
                            tokens.append(self.vocab_ids[w])
                        else:
                            term_id = len(self.vocab)
                            self.vocab.append(w)
                            self.vocab_ids[w] = term_id
                            tokens.append(term_id)

                self.doc_snippets.append(line[:200])
                self.docs.append({ 'tokens': tokens })

        self.num_terms = len(self.vocab)
        print("Read {} documents with a total of {} terms".format(self.num_docs, self.num_terms))                
    def make_draw(self, alpha, beta):
        """Makes a single draw from the posterior distribution in an MCMC fashion."""
        for doc_id in range(self.num_docs):
            doc = self.docs[doc_id]
            doc_tokens = doc["tokens"]
            doc_topics = doc["topics"]

            for idx, (token, topic) in enumerate(zip(doc_tokens, doc_topics)):
                self.term_topics[token][topic] -= 1 
                self.doc_topics[doc_id][topic] -= 1 
                self.topic_totals[topic] -= 1
                
                topic_probs = self._compute_topic_probs(doc_id, token, alpha, beta)
                new_topic = self._sample_topic(topic_probs)

                doc_topics[idx] = new_topic
                self.term_topics[token][new_topic] += 1 
                self.doc_topics[doc_id][new_topic] += 1 
                self.topic_totals[new_topic] += 1

        return self
        
    def _compute_topic_probs(self, doc, token, alpha, beta):
        probs = [0] * self.num_topics
        
        for topic in range(self.num_topics):
            factor1 = alpha + self.doc_topics[doc][topic]
            factor2 = beta + self.term_topics[token][topic]
            factor3 = beta * len(self.vocab) + self.topic_totals[topic]            
            probs[topic] = factor1 * factor2 / factor3

        return probs / sum(probs)

    def _sample_topic(self, topic_probs):
        return numpy.random.choice(self.num_topics, size=1, p=topic_probs)[0]
                    
    def compute_logprob(self, alpha, beta):
        """Computes the log marginal posterior."""
        # return super().compute_logprob(alpha, beta)
        K = self.num_topics
        V = len(self.vocab)
        D = self.num_docs

        KV = K * V
        DK = D * K
        VB = V * beta
        KA = K * alpha

        lg = scipy.special.gammaln
        
        term1 = K * lg(VB)
        term2 = -KV * lg(beta)

        term3 = 0
        for topic in range(K):
            for word in range(V):
                term3 += lg(self.term_topics[word][topic] + beta)

        term4 = 0
        for topic in range(K):
            inner_sum = 0
            for word in range(V):
                inner_sum += self.term_topics[word][topic]             
            term4 += lg(inner_sum + beta)
        term4 *= -1
        
        term5 = D * lg(KA)
        term6 = -DK * lg(alpha)

        term7 = 0
        for doc in range(D):
            for topic in range(K):
                term7 = lg(self.doc_topics[doc][topic] + alpha)

        term8 = 0
        for doc in range(D):
            inner_sum = 0
            for topic in range(K):
                inner_sum += self.doc_topics[doc][topic]
            term8 += lg(inner_sum + alpha)
        term8 *= -1

        return term1 + term2 + term3 + term4 + term5 + term6 + term7 + term8
    
    def run(self, num_iterations = 50, alpha = 0.1, beta = 0.01):
        self.logprobs = []

        for iteration in range(num_iterations):
            self.make_draw(alpha, beta)
            logprob = self.compute_logprob(alpha, beta)
            self.logprobs.append(logprob)
            # print("iteration {}, {}".format(iteration, logprob))
            
    def print_topics(self, j):
        """Prints topic distributions for the."""
        topic_term = numpy.array(self.term_topics).T        
        for topic in range(self.num_topics):
            print("Topic %i:" % (topic + 1,), end=" ")
            for word in numpy.argsort(topic_term[topic, :])[::-1][:j]:
                print(self.vocab[word], end=" ")
            print()

    def plot(self):
        plt.plot(self.logprobs)
        plt.ylabel("Log Probability")
        plt.xlabel("# of iterations")
        plt.show()


def main():
    dfile = "../data/sotu_1975_2000.txt"
    swfile = "../data/stoplist_en.txt"
    topics = 10
    top_words = 10
    iterations = 10
    
    model = MyGibbs(topics, dfile, swfile)
    model.run(iterations)

    model.print_topics(top_words)
    # model.plot()

        
if __name__ == "__main__":
    main()
