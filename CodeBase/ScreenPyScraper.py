import json

import nltk
import pandas as pd
import spacy
import seaborn as sns
import colorcet as cc
import regex as re
from CodeBase.Scraper import Scraper

# nlp = spacy.load("en_core_web_trf") #slow but more accurate
nlp = spacy.load("en_core_web_sm") #fast but less accurate


class ScreenPyScrapper(Scraper):
    """
    Child Class of Scraper that scrapes the formatting provided by screenPy and creates the dictionary for
    quick conversion to a dataframe
    Attributes:
        screenplay : Dictionary that holds all the data of the screenplay
            sentence_index : the index of the sentence in relation to the full screenplay
            type : The denotion of if the text is heading or dialogue as denoted by HEADING or CHARCTER
            terior : The current scene's location type of INT./EXT.
            heading : The master location of the scene
            subheading : The secondary heading of the scene
            ToD : The scene denoted time of day.
        location_list : A list holding the index of all scene changes
        sentences : A list holding all the raw text of the screenplay.
    """
    def __init__(self,dirpath,file_path):
        self.dir_path=dirpath
        try:

            with file_path.open("r", encoding="utf-8") as file:
                self.data = json.load(file)
                # print(self.data[0])
            self.filename=file_path.name
        except FileNotFoundError:
            print(file_path+ " was not found.")
    def screenplay_scrape(self):
        """
        Scraping the json file generated from Screenpy scraper.
        The scraping process extracts and structures these elements for further analysis or processing.

        """
        self.screenplay = {'sentence_index': [], 'type': [], 'terior': [], 'heading': [], 'subheading': [], 'ToD': [],
                      'text': []}
        basic = {'ToD': None, 'shot type': None, 'location': None, 'terior': None, 'subj': None}
        self.location_list = []
        self.sentences=[]
        i = 0
        sent_idx = 0
        for scene in self.data:
            location = scene[0]["head_text"]
            self.location_list.append(i)
            # print(i, location)
            for screen in scene:
                if screen["head_type"] == 'heading':
                    # if screen['head_text']['subj'] == 'FADE IN':
                    #     #                 print(screen)
                    #     continue
                    self.screenplay['type'].append(screen["head_type"].upper())
                    # print(screen['head_text'])
                    if screen['head_text'] != location and screen['head_text']['terior'] is not None:
                        # print(i, location)
                        location = screen['head_text']
                        self.location_list['index'].append(i)

                elif screen["head_type"] == 'speaker/title':
                    self.screenplay['type'].append(str(screen["head_text"]['speaker/title'].split('(')[0].strip()))
                else:
                    continue
                process_text = str(screen['text'].strip())
                sent = nltk.sent_tokenize(process_text)
                sent_idx += len(sent)
                self.sentences.extend(sent)
                self.screenplay["sentence_index"].append(sent_idx)
                self.screenplay['text'].append(process_text)
                try:
                    if location['terior'] is not None:
                        self.screenplay['terior'].append(location['terior'])
                    else:
                        self.screenplay['terior'].append("")
                except KeyError:
                    self.screenplay['terior'].append("")
                try:
                    if location['location'] is not None:
                        self.screenplay['heading'].append(str(location['location'][0]))
                    else:
                        self.screenplay['heading'].append("")
                except KeyError:
                    self.screenplay['heading'].append("")
                try:
                    if location['location'] is not None and len(location['location']) > 1:
                        self.screenplay['subheading'].append(str(location['location'][1:]))
                    else:
                        self.screenplay['subheading'].append("")
                except KeyError:
                    self.screenplay['subheading'].append("")
                try:
                    if location['ToD'] is not None:
                        self.screenplay['ToD'].append(location['ToD'])
                    else:
                        self.screenplay['ToD'].append("")
                except KeyError:
                    self.screenplay['ToD'].append("")
                # screenplay['text'].append(nlp(screen['text']))
                i += 1
        temp = set(self.location_list)
        self.location_list = list(temp)
        self.location_list.sort()
        # print(self.location_list)
    def get_json_data(self):
        return self.screenplay,self.characterdict,self.location_list