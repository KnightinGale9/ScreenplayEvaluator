import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import spacy

from CodeBase.Evaluator import Evaluator

# nlp = spacy.load("en_core_web_trf") #slow but more accurate
nlp = spacy.load("en_core_web_sm") #fast but less accurate
class PartOfSpeech(Evaluator):
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
    def __init__(self, scraper):
        super().__init__(scraper)
        self.pos_full={  "ADJ": "adjective",
                    "ADP": "adposition",
                    "ADV": "adverb",
                    "AUX": "auxiliary",
                    "CONJ": "conjunction",
                    "CCONJ": "coordinating conjunction",
                    "DET": "determiner",
                    "INTJ": "interjection",
                    "NOUN": "noun",
                    "PRON": "pronoun",
                    "PROPN": "proper noun",
                    "SCONJ": "subordinating conjunction",
                    "VERB": "verb",
                    "AFX": "affix",
                    "CC": "conjunction, coordinating",
                    "CD": "cardinal number",
                    "DT": "determiner",
                    "EX": "existential there",
                    "FW": "foreign word",
                    "IN": "conjunction, subordinating or preposition",
                    "JJ": "adjective (English), other noun-modifier (Chinese)",
                    "JJR": "adjective, comparative",
                    "JJS": "adjective, superlative",
                    "MD": "verb, modal auxiliary",
                    "NN": "noun, singular or mass",
                    "NNP": "noun, proper singular",
                    "NNPS": "noun, proper plural",
                    "NNS": "noun, plural",
                    "PDT": "predeterminer",
                    "POS": "possessive ending",
                    "PRP": "pronoun, personal",
                    "PRP$": "pronoun, possessive",
                    "RB": "adverb",
                    "RBR": "adverb, comparative",
                    "RBS": "adverb, superlative",
                    "RP": "adverb, particle",
                    "TO": 'infinitival "to"',
                    "UH": "interjection",
                    "VB": "verb, base form",
                    "VBD": "verb, past tense",
                    "VBG": "verb, gerund or present participle",
                    "VBN": "verb, past participle",
                    "VBP": "verb, non-3rd person singular present",
                    "VBZ": "verb, 3rd person singular present",
                    "WDT": "wh-determiner",
                    "WP": "wh-pronoun, personal",
                    "WP$": "wh-pronoun, possessive",
                    "WRB": "wh-adverb",
                    "SP": "space (English), sentence-final particle (Chinese)",
                    "ADD": "email",
                    "NFP": "superfluous punctuation",
                    "GW": "additional word in multi-word expression",
                    "BES": 'auxiliary "be"',
                    "HVS": 'forms of "have"',
                    }

    def run_evaluator(self):
        self.pos_aggregate()
        self.part_of_speech_investigation()
        self.tag_investigation()
        print("Spacy Part of Speech",end="")
    def pos_aggregate(self):
        """
        Goes throughout the whole screenplay and aggregaes the pos count, pos collat, and tag count.
        Initalizes self.pos_count, self.pos_collat, and self.tag_count
        """
        self.pos_count = {
            'ADJ': 0, 'ADP': 0, 'ADV': 0, 'AUX': 0, 'CCONJ': 0, 'DET': 0, 'INTJ': 0,
            'NOUN': 0, 'NUM': 0, 'PART': 0, 'PRON': 0, 'PROPN': 0, 'PUNCT': 0,
            'SCONJ': 0, 'SPACE': 0, 'SYM': 0, 'VERB': 0, 'X': 0
        }
        self.pos_collat = {
            'ADJ': {}, 'ADP': {}, 'ADV': {}, 'AUX': {}, 'CCONJ': {}, 'DET': {}, 'INTJ': {},
            'NOUN': {}, 'NUM': {}, 'PART': {}, 'PRON': {}, 'PROPN': {}, 'PUNCT': {},
            'SCONJ': {}, 'SPACE': {}, 'SYM': {}, 'VERB': {}, 'X': {}
        }
        self.tag_count = {}

        for idx, row in self.scraper.get_fulldf().iterrows():
            pos = nlp(row['text'])
            for token in pos:
                # print(token.text, token.pos_, token.tag_)
                self.pos_count[token.pos_] += 1
                if token.text not in self.pos_collat[token.pos_]:
                    self.pos_collat[token.pos_][token.text.lower()] = 0
                self.pos_collat[token.pos_][token.text.lower()] += 1
                if token.tag_ not in self.tag_count:
                    self.tag_count[token.tag_] = 0
                self.tag_count[token.tag_] += 1
        # print(self.tag_count)
    def get_json_data(self):
        """
        A function to retrieve the data created by sentiment analysis for Screenplay_Raw_data.json
        :return: {"PartOfSpeech":self.pos_count,"word_in_partofspeech":self.pos_collat,"Tag_Count":self.tag_count}
        """
        return {"partofspeech":{"PartOfSpeech":self.pos_count,
                "word_in_partofspeech":self.pos_collat,
                "Tag_Count":self.tag_count}}

    def part_of_speech_investigation(self):
        """
        Creates a csv file which shows the values for each part of speech. It shows count,percentage, and gini index.
        :returns: None (Creates the file with the extension -pos_data.csv)
        """
        keep = []
        for k in self.pos_count:
            if k in self.pos_full:
                keep.append(k)
        temp_dict = dict((k, self.pos_count[k]) for k in keep)
        posss = pd.DataFrame()
        posss["Part of Speech"] = [self.pos_full[k] for k in temp_dict]
        posss["values"] = temp_dict.values()
        posss["percent"] = posss['values'] / posss['values'].sum()
        posss.set_index("Part of Speech", inplace=True)
        gini_val = {}
        for key in temp_dict:
            gini_val[key] = self.gini(key)
        posss["gini"] = gini_val.values()
        posss.loc["total"] = [posss['values'].sum(), np.nan, np.nan]
        posss.to_csv(f'{self.scraper.get_output_dir()}/{self.replace_file_extension("-pos_data.csv")}')

    def tag_investigation(self):
        """
        Creates a csv file which shows the values for each tagged part of speech.
        It shows count,percentage, and gini index.
        :returns: None (Creates the file with the extension -pos_data.csv)
        """
        posss = pd.DataFrame()
        keep = []
        for k in self.tag_count:
            if k in self.pos_full:
                keep.append(k)
        temp_dict= dict((k, self.tag_count[k]) for k in keep)
        posss["Part of Speech"] = [self.pos_full[k] for k in temp_dict]
        posss["values"] = temp_dict.values()
        posss["percent"] = posss['values'] / posss['values'].sum()
        posss.set_index("Part of Speech", inplace=True)
        posss.loc["total"] = [posss['values'].sum(), np.nan]
        posss.to_csv(f'{self.scraper.get_output_dir()}/{self.replace_file_extension("-tag_data.csv")}')

    def gini(self,pos):
        """
        Calculates the gini index for the given part of speech distribution.
        :param pos: pos count
        :return: gini index
        """
        pos_list = list(self.pos_collat[pos.upper()].items())
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
