import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from nltk import CoreNLPParser

from CodeBase.Evaluator import Evaluator

# nlp = spacy.load("en_core_web_trf") #slow but more accurate
class POSCoreNLP(Evaluator):
    """
    An evaluator that aggregates the part of speech tags used in the screenplay.

    Part of Speech distribution of each tag type enables us to gain insights into the compositional makeup
    of a screenplay. Using Part of Speech can understand the raw distribution and gini index for each tag.
    Attributes:
        pos_full: Dictionary of all the abreviation used by Spacy to improve pie charts
        pos_count: Dictionary of the count of pos
        pos_collat: Dictionary of each word from each tag and their coint
        tag_count: Dictionary of the count of each tag
    """
    def __init__(self, scraper,tree=None):
        super().__init__(scraper)
        self.sentences = self.scraper.get_sentences()
        #https://docs.datasaur.ai/assisted-labeling/ml-assisted-labeling/corenlp-pos
        self.pos_full={
        "CC": "conjunction, coordinating",
        "CD": "Cardinal number",
        "DT": "Determiner",
        "EX": "Existential there",
        "FW": "Foreign word",
        "IN": "Preposition or subordinating conjunction",
        "JJ": "Adjective",
        "JJR": "Adjective, comparative",
        "JJS": "Adjective, superlative",
        "LS": "List item marker",
        "MD": "Modal verb",
        "NN": "Noun, singular or mass",
        "NNS": "Noun, plural",
        "NNP": "Proper noun, singular",
        "NNPS": "Proper noun, plural",
        "PDT": "Predeterminer",
        "POS": "Possessive ending",
        "PRP": "Personal pronoun",
        "PRP$": "Possessive pronoun",
        "RB": "Adverb",
        "RBR": "Adverb, comparative",
        "RBS": "Adverb, superlative",
        "RP": "Particle",
        "SYM": "Symbol",
        "TO": "to (as in ‘to go’)",
        "UH": "Interjection",
        "VB": "Verb, base form",
        "VBD": "Verb, past tense",
        "VBG": "Verb, gerund or present participle",
        "VBN": "Verb, past participle",
        "VBP": "Verb, non-3rd person singular present",
        "VBZ": "Verb, 3rd person singular present",
        "WDT": "Wh-determiner",
        "WP": "Wh-pronoun",
        "WP$": "Possessive wh-pronoun",
        "WRB": "Wh-adverb"
                    }
        self.premade_tree=tree


    def run_evaluator(self):
        self.pos_aggregate()
        self.part_of_speech_investigation()
        # self.tag_investigation()
        print("CoreNLP Part of Speech",end="")
    def pos_aggregate(self):
        """
        Goes throughout the whole screenplay and aggregaes the pos count, pos collat, and tag count.
        Initalizes self.pos_count, self.pos_collat, and self.tag_count
        """
        self.pos_count = {
           "CC":0,"CD": 0, "DT": 0, "EX": 0, "FW": 0, "IN": 0, "JJ": 0, "JJR": 0, "JJS": 0, "LS": 0, "MD": 0,
            "NN": 0, "NNS": 0, "NNP": 0, "NNPS": 0, "PDT": 0, "POS": 0, "PRP": 0, "PRP$": 0, "RB": 0,
            "RBR": 0, "RBS": 0, "RP": 0, "SYM": 0, "TO": 0, "UH": 0, "VB": 0, "VBD": 0, "VBG": 0,
            "VBN": 0, "VBP": 0, "VBZ": 0, "WDT": 0, "WP": 0, "WP$": 0, "WRB": 0
        }
        self.pos_collat = {
            "CC":{},"CD": {}, "DT": {}, "EX": {}, "FW": {}, "IN": {}, "JJ": {}, "JJR": {}, "JJS": {}, "LS": {}, "MD": {},
            "NN": {}, "NNS": {}, "NNP": {}, "NNPS": {}, "PDT": {}, "POS": {}, "PRP": {}, "PRP$": {}, "RB": {},
            "RBR": {}, "RBS": {}, "RP": {}, "SYM": {}, "TO": {}, "UH": {}, "VB": {}, "VBD": {}, "VBG": {},
            "VBN": {}, "VBP": {}, "VBZ": {}, "WDT": {}, "WP": {}, "WP$": {}, "WRB": {}}
        tss={}
        CORENLP_URL = 'http://localhost:9000'

        # Check if CoreNLP server is running
        try:
            response = requests.get(CORENLP_URL)
            # if response.status_code != 200:
            #     raise ConnectionError(f"CoreNLP server responded with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(
                f"Could not connect to CoreNLP server at {CORENLP_URL}. Make sure it is running.") from e

        parser = CoreNLPParser(url=CORENLP_URL)
        for i, s in enumerate(self.sentences):
            # if not s.strip(): continue
            if self.premade_tree is None:
                try:
                    t = list(parser.raw_parse(s))[0]
                except Exception as ex:
                    print(type(ex), "skipping", s)
                    continue
            else:
                t = self.premade_tree[i]
            for subtree in t.subtrees():
                if len(subtree) == 1 and isinstance(subtree[0], str):  # Leaf node (word)
                    word = subtree[0].lower()  # Normalize case
                    pos_tag = subtree.label()  # Get POS tag

                    # print(word,pos_tag)
                    if pos_tag in self.pos_full:
                        # Update POS count
                        self.pos_count[pos_tag] += 1

                        if word not in self.pos_collat[pos_tag]:
                            self.pos_collat[pos_tag][word] = 0

                        # Update POS-word mapping
                        self.pos_collat[pos_tag][word] += 1
                    # else:
                    #     if pos_tag not in tss:
                    #         tss[pos_tag]=[]
                    #     tss[pos_tag].append(word)
                    #     print("skip",word,pos_tag)
        # print(tss)

    def get_json_data(self):
        """
        A function to retrieve the data created by sentiment analysis for Screenplay_Raw_data.json
        :return: {"PartOfSpeech":self.pos_count,"word_in_partofspeech":self.pos_collat,"Tag_Count":self.tag_count}
        """
        return {"partofspeech":{"PartOfSpeech":self.pos_count,
                "word_in_partofspeech":self.pos_collat}}

    def part_of_speech_investigation(self):
        """
        Creates a csv file which shows the values for each part of speech. It shows count,percentage, and gini index.
        :returns: None (Creates the file with the extension -pos_data.csv)
        """
        categories = {
            "Adjective": ["JJ", "JJR", "JJS"],
            "Adposition": ["IN"],
            "Adverb": ["RB", "RBR", "RBS"],
            "Auxiliary": ["MD"],
            "Coordinating Conjunction": ["CC"],
            "Determiner": ["DT", "PDT", "WDT"],
            "Interjection": ["UH"],
            "Noun": ["NN", "NNS"],
            "Pronoun": ["PRP", "PRP$", "WP", "WP$"],
            "Proper Noun": ["NNP", "NNPS"],
            # "Subordinating Conjunction": ["IN"],  # Note: "IN" appears under both Adposition and Subordinating Conjunction
            "Verb": ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
        }
        self.categories_count={
             "Adjective": 0,
            "Adposition": 0,
            "Adverb": 0,
            "Auxiliary": 0,
            "Coordinating Conjunction": 0,
            "Determiner": 0,
            "Interjection": 0,
            "Noun": 0,
            "Pronoun": 0,
            "Proper Noun": 0,
            # "Subordinating Conjunction": ["IN"],  # Note: "IN" appears under both Adposition and Subordinating Conjunction
            "Verb": 0
        }
        self.categories_colat = {
            "Adjective": {},
            "Adposition": {},
            "Adverb": {},
            "Auxiliary": {},
            "Coordinating Conjunction": {},
            "Determiner": {},
            "Interjection": {},
            "Noun": {},
            "Pronoun": {},
            "Proper Noun": {},
            # "Subordinating Conjunction": ["IN"],  # Note: "IN" appears under both Adposition and Subordinating Conjunction
            "Verb": {}
        }
        for k in categories:
            for i in categories[k]:
                self.categories_count[k] += self.pos_count[i]
                self.categories_colat[k].update(self.pos_collat[i])

        posss = pd.DataFrame()
        posss["Part of Speech"] =  self.categories_count.keys()
        posss["values"] = self.categories_count.values()
        posss["percent"] = posss['values'] / posss['values'].sum()
        posss.set_index("Part of Speech", inplace=True)
        gini_val = {}
        for key in self.categories_count:
            gini_val[key] = self.gini(key)
        posss["gini"] = gini_val.values()
        posss.loc["total"] = [posss['values'].sum(), np.nan, np.nan]
        posss.to_csv(f'{self.scraper.get_output_dir()}/{self.replace_file_extension("-pos_data.csv")}')

    def gini(self,pos):
        """
        Calculates the gini index for the given part of speech distribution.
        :param pos: pos count
        :return: gini index
        """
        pos_list = list(self.categories_colat[pos].items())
        pos_list.sort(key=lambda x: x[1], reverse=True)
        if len(pos_list)==0:
            return 0
        keys, values = zip(*pos_list)
        array = np.sort(values)
        """Calculate the Gini coefficient of a numpy array."""
        # based on bottom eq:
        # http://www.statsdirect.com/help/generatedimages/equations/equation154.svg
        # from:
        # http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
        # All values are treated equally, arrays must be 1d:
        array = array.flatten()
        if np.amin(array) < 0:
            # Values cannot be negative:
            array -= np.amin(array)
        # Values cannot be 0:
        array = array + 0.0000001
        # Values must be sorted:
        array = np.sort(array)
        # Index per array element:
        index = np.arange(1, array.shape[0] + 1)
        # Number of array elements:
        n = array.shape[0]
        # Gini coefficient:
        return ((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array)))
