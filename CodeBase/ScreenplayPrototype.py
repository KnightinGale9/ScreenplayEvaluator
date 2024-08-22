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

from CodeBase.ScreenPyScraper import ScreenPyScrapper
from CodeBase.GraphParent import GraphParent
from CodeBase.IncreasingGraph import IncreasingGraph
from CodeBase.PrescenceGraph import PrescenceGraph
from CodeBase.PartOfSpeech import PartOfSpeech


# nlp = spacy.load("en_core_web_trf") #slow but more accurate
nlp = spacy.load("en_core_web_sm") #fast but less accurate


screenplay_main=ScreenPyScrapper("indianajonesandtheraidersofthelostark.json")
screenplay_main.screenplay_scrape()
screenplay_main.dataframe_creation(character_removal={'PERU','TOP SECRET','DO NOT OPEN!'})

increasinggraph = IncreasingGraph(screenplay_main.filename,screenplay_main.characterdict, screenplay_main.dialoguedf,
                                  screenplay_main.headingdf, screenplay_main.locationdf,screenplay_main.locationcocurence)
prescencegraph = PrescenceGraph(screenplay_main.filename,screenplay_main.characterdict, screenplay_main.dialoguedf,
                                  screenplay_main.headingdf, screenplay_main.locationdf,screenplay_main.locationcocurence)

partofspeech = PartOfSpeech(screenplay_main.filename,screenplay_main.fulldf)

increasinggraph.combined_lines()
increasinggraph.increasing_graph()
prescencegraph.combined_lines()
prescencegraph.set_sorted_character("matrix")
prescencegraph.prescence_graph()


partofspeech.pos_aggregate()
partofspeech.pos_pie_chart()
partofspeech.key_pos_pie_chart()