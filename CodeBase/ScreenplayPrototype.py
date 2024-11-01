import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import nltk
import spacy
from spacy import displacy
import seaborn as sns
import colorcet as cc
from transformers import pipeline
from spacy.tokenizer import Tokenizer
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.interpolate import make_interp_spline
import regex as re

from CodeBase.HeapsLaw import HeapsLaw
from CodeBase.SceneLength import SceneLength
from CodeBase.ScreenPyScraper import ScreenPyScrapper
from CodeBase.GraphParent import GraphParent
from CodeBase.IncreasingGraph import IncreasingGraph
from CodeBase.PrescenceGraph import PrescenceGraph
from CodeBase.PartOfSpeech import PartOfSpeech
from CodeBase.SentenceComplexity import SentenceComplexity
from CodeBase.ChatGPTScraper import ChatGPTScraper
from CodeBase.SentimentAnalysis import SentimentAnalysis

# nlp = spacy.load("en_core_web_trf") #slow but more accurate
nlp = spacy.load("en_core_web_sm") #fast but less accurate


# screenplay_main=ChatGPTScraper("example.txt")
screenplay_main=ScreenPyScrapper("indianajonesandtheraidersofthelostark.json")
screenplay_main.screenplay_scrape()
screenplay_main.dataframe_creation()




# increasinggraph = IncreasingGraph(screenplay_main)
# increasinggraph.combined_lines()
# increasinggraph.increasing_graph()
#
# prescencegraph = PrescenceGraph(screenplay_main)
# prescencegraph.combined_lines()
# prescencegraph.set_sorted_character("matrix")
# prescencegraph.prescence_graph()
#
# scenelength = SceneLength(screenplay_main)
# scenelength.create_scene_length()
# scenelength.graph_over_time()
# scenelength.graph_over_length()
#
# sentimentanalysis = SentimentAnalysis(screenplay_main)
# sentimentanalysis.create_sentiment_list()
# sentimentanalysis.create_graph()
#
# heapslaw = HeapsLaw(screenplay_main)
# heapslaw.heaps_law()
# heapslaw.plot_vocab_growth()
#
# sentencecomplexity = SentenceComplexity(screenplay_main)
# sentencecomplexity.sentence_complexity_calculations()
# sentencecomplexity.sentence_length_graph()
# sentencecomplexity.sentence_length_indexing()
# sentencecomplexity.yngves_and_frazier_mean()

partofspeech = PartOfSpeech(screenplay_main)
partofspeech.pos_aggregate()
partofspeech.pos_pie_chart()
partofspeech.key_pos_pie_chart()
partofspeech.noun_pie_chart()
partofspeech.adj_pie_chart()
partofspeech.adverb_pie_chart()
partofspeech.verb_pie_chart()
