'''
A program to calculate syntactic complexity of parse trees. (Relies on NLTK)
This is an implementation of some of the methods in:

Syntactic complexity measures for detecting Mild Cognitive Impairment
Brian Roark, Margaret Mitchell and Kristy Hollingshead
Proc BioNLP 2007.
'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import sys

from scipy.interpolate import make_interp_spline

try:
    from nltk.tree import Tree
    from nltk.draw.tree import TreeWidget
    from nltk.draw.util import (CanvasFrame, CanvasWidget, BoxWidget,
                                TextWidget, ParenWidget, OvalWidget)
    from nltk.parse import CoreNLPParser
    from CodeBase.GraphParent import GraphParent

    import nltk
except ImportError:
    print('Error: cannot import the NLTK!')
    print('You need to install the NLTK. Please visit http://nltk.org/install.html for details.')
    print("On Ubuntu, the installation can be done via 'sudo apt-get install python-nltk'")
    sys.exit()

N_BINS = 20

import json
class SentenceComplexity(GraphParent):
    """
    An evaluator that calculates and visualizes the sentence complexity.
    The code for complexity scores for ygnves and frazier is from
    Brian Roark, Margaret Mitchell and Kristy Hollingshead
    Proc BioNLP 2007.
    Sentence complexity refers to the structural intricacy of a sentence,
    often measured by factors such as the depth of its syntactic tree,
    the number of embedded clauses, and the relationships between words.
    It is used to assess readability, linguistic richness, and cognitive load.
    Attributes:
        yngves: A list storing the ygnves score for each sentence
        fraziers:A list storing the frazier score for each sentence
        wordss:A list storing the word count for each sentence
        yngve_avg: the average of all yngve score
        frazier_avg: the average of all frazier score
        words_avg: the average of all word count
    """
    def run_evaluator(self):
        self.sentence_complexity_calculations()
        self.sentence_length_graph()
        self.sentence_length_indexing()
        self.yngves_and_frazier_mean()
        print("Sentence Complexity",end="")
    def calc_words(self,t):
        """
        Brian Roark, Margaret Mitchell and Kristy Hollingshead
        Proc BioNLP 2007.
        """
        if type(t) == str:
            return 1
        else:
            val = 0
            for child in t:
                val += self.calc_words(child)
            return val

    def calc_nodes(self,t):
        """
        Brian Roark, Margaret Mitchell and Kristy Hollingshead
        Proc BioNLP 2007.
        """
        if type(t) == str:
            return 0
        else:
            val = 0
            for child in t:
                val += self.calc_nodes(child) + 1
            return val

    def calc_yngve(self,t, par):
        """
        Brian Roark, Margaret Mitchell and Kristy Hollingshead
        Proc BioNLP 2007.
        """
        if type(t) == str:
            return par
        else:
            val = 0
            for i, child in enumerate(reversed(t)):
                val += self.calc_yngve(child, par+i)
            return val

    def is_sent(self,val):
        """
        Brian Roark, Margaret Mitchell and Kristy Hollingshead
        Proc BioNLP 2007.
        """
        return len(val) > 0 and val[0] == "S"

    def calc_frazier(self,t, par, par_lab):
        """
        Brian Roark, Margaret Mitchell and Kristy Hollingshead
        Proc BioNLP 2007.
        """
        # print t
        # print par
        if type(t) == str:
            # print par-1
            return par-1
        else:
            val = 0
            for i, child in enumerate(t):
                # For all but the leftmost child, zero
                score = 0
                if i == 0:
                    my_lab = t.label()
                    # If it's a sentence, and not duplicated, add 1.5
                    if self.is_sent(my_lab):
                        score = (0 if self.is_sent(par_lab) else par+1.5)
                    # Otherwise, unless it's a root node, add one
                    elif my_lab != "" and my_lab != "ROOT" and my_lab != "TOP":
                        score = par + 1
                val += self.calc_frazier(child, score, my_lab)
            return val

    def __init__(self,scraper,tree=None):
        super().__init__(scraper)
        self.sentences=self.scraper.get_sentences()

        self.premade_tree=tree
    def sentence_complexity_calculations(self):
        """
        Modified code to fit the evaluator from
        Brian Roark, Margaret Mitchell and Kristy Hollingshead
        Proc BioNLP 2007.
        
        Calculates the frazier and ygnves score for each sentence.
        Initalizes yngves, fraziers, wordss, yngve_avg, frazier_avg, and words_avg.
        """
        sents = 0
        words_tot = 0
        yngve_tot = 0
        frazier_tot = 0
        nodes_tot = 0
        self.yngves = []
        self.fraziers = []
        self.wordss = []

        CORENLP_URL = 'http://localhost:9000'

        # Check if CoreNLP server is running
        try:
            response = requests.get(CORENLP_URL)
            # if response.status_code != 200:
            #     raise ConnectionError(f"CoreNLP server responded with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(
                f"Could not connect to CoreNLP server at {CORENLP_URL}. Make sure it is running.") from e

        # Initialize parser after confirming server is running
        parser = CoreNLPParser(url=CORENLP_URL)
        for i,s in enumerate(self.sentences):
            # if not s.strip(): continue
            if self.premade_tree is None:
                try:
                    t = list(parser.raw_parse(s))[0]
                except Exception as ex:
                    print(type(ex),"skipping", s)
                    continue
            else:
                t= self.premade_tree[i]

            words = self.calc_words(t)
            words_tot += words
            sents += 1
            self.wordss.append(words)
            yngve = self.calc_yngve(t, 0)
            yngve_avg = float(yngve)/words
            yngve_tot += yngve_avg
            self.yngves.append(yngve)
            nodes = self.calc_nodes(t)
            nodes_avg = float(nodes)/words
            nodes_tot += nodes_avg
            frazier = self.calc_frazier(t, 0, "")
            frazier_avg = float(frazier)/words
            frazier_tot += frazier_avg
            self.fraziers.append(frazier)
            # print "Sentence=%d\twords=%d\tyngve=%f\tfrazier=%f\tnodes=%f" % (sents, words, yngve_avg, frazier_avg, nodes_avg)
        self.yngve_avg = float(yngve_tot)/sents
        self.frazier_avg = float(frazier_tot)/sents
        nodes_avg = float(nodes_tot)/sents
        self.words_avg = float(words_tot)/sents
        # print("Total\tsents=%d\twords=%f\tyngve=%f\tfrazier=%f\tnodes=%f" % (sents, words_avg, yngve_avg, frazier_avg, nodes_avg))

        data = {"yngves": self.yngves, "fraziers": self.fraziers, "words": self.wordss}
        self.sentence_data_df =pd.DataFrame()
        for i in data:
            self.sentence_data_df[i]=data[i]
        self.sentence_data_df["yngves_mean"]=self.sentence_data_df['yngves']/self.sentence_data_df['words']
        self.sentence_data_df["fraziers_mean"] = self.sentence_data_df['fraziers'] / self.sentence_data_df['words']
        # print(sents,self.sentence_data_df)
    def get_json_data(self):
        """
        A function to retrieve the data created by sentence complexity for Screenplay_Raw_data.json
        :return: {"yngves": self.yngves, "fraziers": self.fraziers, "words": self.wordss,
                   "averages": {"yngve": self.yngve_avg, "frazier": self.frazier_avg, "words": self.words_avg}}
        """
        return {"sentencecomplexity":{"yngves": self.yngves, "fraziers": self.fraziers, "words": self.wordss,
                   "averages": {"yngve": self.yngve_avg, "frazier": self.frazier_avg, "words": self.words_avg}}}
    def sentence_length_indexing(self):
        """
        Creates a bar plot of sentence length by word count.
        X-axis is denoted by Sentence length by word. Y-axis is denoted by Count.
        :returns: None (Creates the file with the extension -SentenceWordCount.png)
        """
        sentence_length = {}
        for idx, line in self.sentence_data_df.iterrows():
            line_length = line['words']
            if line_length not in sentence_length:
                sentence_length[line_length] = 0
            sentence_length[line_length] += 1

        sorted_sentence = list(sentence_length.items())
        sorted_sentence.sort()
        keys, values = zip(*sorted_sentence)
        fig, ax = plt.subplots(figsize=(20, 10))

        plt.bar(keys, values)
        plt.title("Sentence Length by Word Count")
        ax.set_xlabel("Sentence Length by Word")
        ax.set_ylabel("Count")
        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-SentenceWordCount.png")}',bbox_inches='tight')
        plt.close()
    def sentence_length_graph(self):
        """
        Creates a scatter plot of sentence length by over time.
        X-axis is denoted by Sentence index. Y-axis is denoted by sentence length by word.
        :returns: None (Creates the file with the extension -SentenceWordCountOverTime.png)
        """
        fig, ax = plt.subplots(figsize=(20, 10))

        keys, values = self.sentence_data_df.index, self.sentence_data_df['words']
        spl = make_interp_spline(keys, values, k=3)  # k=3 indicates a cubic spline
        plt.xticks(np.append([0], list(self.scraper.get_locationdf()['sentence_index'])))
        plt.scatter(keys, values,label = "sentence_length")

        plt.xlim([0, self.scraper.get_locationdf()['sentence_index'].iloc[-1]])

        self.x_axis_alt_bands()
        plt.xticks(list(range(0,list(self.scraper.get_locationdf()['sentence_index'])[-1], 500)))
        plt.title("Sentence Length by Word Index")
        ax.set_ylabel("Sentence Length by Word")
        ax.set_xlabel("Sentence Index")
        plt.legend()
        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-SentenceWordCountOverTime.png")}',bbox_inches='tight')
        plt.close()
    def yngves_and_frazier_mean(self):
        """
        Creates a scatter plot of sentence compexity of ygnves and frazier score.
        X-axis is denoted by Sentence index. Y-axis is denoted by complexity score.
        :returns: None (Creates the file with the extension -yngves_and_frazier_mean.png)
        """
        # plt.rcParams['font.size'] = 16  # Adjust size as needed

        fig, ax = plt.subplots(figsize=(20, 10))

        keys, values = self.sentence_data_df.index, self.sentence_data_df['yngves_mean']

        plt.scatter(keys, values,label = "yngves_mean")
        keys, values = self.sentence_data_df.index, self.sentence_data_df['fraziers_mean']
        plt.scatter(keys, values,label = "fraziers_mean")

        plt.xticks(np.append([0], list(self.scraper.get_locationdf()['sentence_index'])))

        plt.xlim([0, self.scraper.get_locationdf()['sentence_index'].iloc[-1]])
        self.x_axis_alt_bands()
        plt.xticks(list(range(0,list(self.scraper.get_locationdf()['sentence_index'])[-1], 500)))

        plt.title("Yngves and Frazier mean score")
        ax.set_xlabel('Sentence Index')
        ax.set_ylabel('Complexity Score')
        ax.legend(fontsize=16)  # Adjust the font size as needed
        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-yngves_and_frazier_mean.png")}')
        plt.close()