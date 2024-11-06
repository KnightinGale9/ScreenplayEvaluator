import matplotlib.pyplot as plt
import spacy

from CodeBase.Evaluator import Evaluator

# nlp = spacy.load("en_core_web_trf") #slow but more accurate
nlp = spacy.load("en_core_web_sm") #fast but less accurate
class PartOfSpeech(Evaluator):

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
                    "NUM": "numeral",
                    "PART": "particle",
                    "PRON": "pronoun",
                    "PROPN": "proper noun",
                    "PUNCT": "punctuation",
                    "SCONJ": "subordinating conjunction",
                    "SYM": "symbol",
                    "VERB": "verb",
                    "X": "other",
                    "EOL": "end of line",
                    "SPACE": "space",
                    ".": "punctuation mark, sentence closer",
                    ",": "punctuation mark, comma",
                    "-LRB-": "left round bracket",
                    "-RRB-": "right round bracket",
                    "``": "opening quotation mark",
                    '""': "closing quotation mark",
                    "''": "closing quotation mark",
                    ":": "punctuation mark, colon or ellipsis",
                    "$": "symbol, currency",
                    "#": "symbol, number sign",
                    "AFX": "affix",
                    "CC": "conjunction, coordinating",
                    "CD": "cardinal number",
                    "DT": "determiner",
                    "EX": "existential there",
                    "FW": "foreign word",
                    "HYPH": "punctuation mark, hyphen",
                    "IN": "conjunction, subordinating or preposition",
                    "JJ": "adjective (English), other noun-modifier (Chinese)",
                    "JJR": "adjective, comparative",
                    "JJS": "adjective, superlative",
                    "LS": "list item marker",
                    "MD": "verb, modal auxiliary",
                    "NIL": "missing tag",
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
                    "XX": "unknown",
                    "BES": 'auxiliary "be"',
                    "HVS": 'forms of "have"',
                    "_SP": "whitespace"}

    def pos_aggregate(self):
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
        for i in ['SPACE', 'SYM', 'X', 'PUNCT', 'NUM']:
            self.pos_count.pop(i)
        # print(self.tag_count)
    def get_json_data(self):
        return self.pos_count,self.pos_collat,self.tag_count
    def pos_pie_chart(self):
        labels = []
        sizes = []
        for temp in self.pos_count.keys():
            labels.append(self.pos_full[temp])
            sizes.append(self.pos_count[temp])
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.savefig(f'../output/{self.scraper.get_filename().replace(".json", "-pos-piechart.png")}')
        plt.close()

    def key_pos_pie_chart(self):
        keys_to_keep = ["NOUN", "ADV", "ADJ", "VERB"]
        subset_dict = {k: self.pos_count[k] for k in keys_to_keep if k in self.pos_count}

        labels = []
        sizes = []
        for temp in subset_dict.keys():
            labels.append(self.pos_full[temp])
            sizes.append(self.pos_count[temp])

        fig, ax = plt.subplots()
        # plt.title("Noun")
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.savefig(f'../output/{self.scraper.get_filename().replace(".json", "-curated-pos-piechart.png")}')
        plt.close()

    def noun_pie_chart(self):
        keys_to_keep = ["NN", "NNP", "NNPS", "NNS"]
        subset_dict = {k: self.tag_count[k] for k in keys_to_keep if k in self.tag_count}

        labels = []
        sizes = []
        for temp in subset_dict.keys():
            labels.append(self.tag_count[temp])
            sizes.append(self.tag_count[temp])

        fig, ax = plt.subplots()
        plt.title("Noun")
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.savefig(f'../output/{self.scraper.get_filename().replace(".json", "-noun-piechart.png")}')
        plt.close()

    def adj_pie_chart(self):
        keys_to_keep = ["JJ", "JJR", "JJS"]
        subset_dict = {k: self.tag_count[k] for k in keys_to_keep if k in self.tag_count}

        labels = []
        sizes = []
        for temp in subset_dict.keys():
            labels.append(self.pos_full[temp])
            sizes.append(self.tag_count[temp])

        fig, ax = plt.subplots()
        plt.title("adjective")
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.savefig(f'../output/{self.scraper.get_filename().replace(".json", "-adj-piechart.png")}')
        plt.close()

    def verb_pie_chart(self):
        keys_to_keep = ["MD", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
        subset_dict = {k: self.tag_count[k] for k in keys_to_keep if k in self.tag_count}

        labels = []
        sizes = []
        for temp in subset_dict.keys():
            labels.append(self.pos_full[temp])
            sizes.append(self.tag_count[temp])

        fig, ax = plt.subplots()
        plt.title("Verb")
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.savefig(f'../output/{self.scraper.get_filename().replace(".json", "-verb-piechart.png")}')
        plt.close()


    def adverb_pie_chart(self):
        keys_to_keep = ["RB", "RBR", "RBS", "RP", "WRB"]
        subset_dict = {k: self.tag_count[k] for k in keys_to_keep if k in self.tag_count}

        labels = []
        sizes = []
        for temp in subset_dict.keys():
            labels.append(self.pos_full[temp])
            sizes.append(self.tag_count[temp])

        fig, ax = plt.subplots()
        plt.title("Adverb")
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.savefig(f'../output/{self.scraper.get_filename().replace(".json", "-adverb-piechart.png")}')
        plt.close()
