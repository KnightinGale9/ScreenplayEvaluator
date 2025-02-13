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
    def __init__(self,dirpath,file_path):
        self.dir_path=dirpath
        try:
            f = open(file_path)
            self.data = json.load(f)
            match = re.search(r"\/(.*)$", file_path)
            if match:
                self.filename=match.group(1)  # Access group 1
                print(self.filename)
            f.close()
        except FileNotFoundError:
            print(file_path+ " was not found.")
    def screenplay_scrape(self):
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
    # def dataframe_creation(self):
    #
    #     self.fulldf = pd.DataFrame(self.screenplay)
    #     self.fulldf.drop(self.fulldf.loc[self.fulldf['text'] == ""].index, inplace=True)
    #     character_set = set(self.fulldf.loc[self.fulldf['type'] != "HEADING"]['type'])
    #     sorted_character = list(character_set)
    #     sorted_character.sort()
    #     sorted_character = [k for k in sorted_character]
    #     palette = sns.color_palette(cc.glasbey, n_colors=len(character_set))
    #     #character dict
    #     self.characterdict = dict(zip(sorted_character, palette))
    #     if "" in self.characterdict:
    #         self.characterdict.pop("")
    #         for idx, row in self.fulldf.loc[self.fulldf['type'] == ""].iterrows():
    #             self.fulldf.loc[idx, "text"] = str(row['type'] + " " + row['text'])
    #             self.fulldf.loc[idx, 'type'] = "HEADING"
    #     print(self.fulldf)
    #     self.dialoguedf = self.fulldf.loc[self.fulldf['type'] != "HEADING"].copy()
    #
    #     self.headingdf = self.fulldf.loc[self.fulldf['type'] == "HEADING"].copy()
    #     heading_character = []
    #
    #     characterset = set(self.characterdict.keys())
    #
    #
    #     for idx, row in self.headingdf.iterrows():
    #         # print(idx,row['text'].upper())
    #         nlpset = set()
    #         # nlpset.add()
    #         # print(row['text'].upper())
    #         for token in nlp(row['text'].upper()):
    #             nlpset.add(token.lemma_.upper())
    #         heading_character.append(characterset.intersection(nlpset).copy())
    #         # if idx == 80:
    #         #     print(heading_character[-1], nlpset)
    #     self.headingdf = self.headingdf.assign(characters=heading_character)
    #     #location df
    #
    #     locationdf = self.fulldf[self.fulldf.index.isin(self.location_list)].copy()
    #
    #     # locationdf.loc[:, locationdf.columns != 'location']
    #     locationchar = []
    #     characterprescene = {key: [] for key in self.characterdict.keys()}
    #     wclist = self.location_list[1:].copy()
    #     wclist.append(len(self.fulldf))
    #
    #     for start, end in zip(self.location_list, wclist):
    #         intermidiate = set(self.fulldf.loc[start:end]['type']).difference(set(["HEADING"]))
    #         intermidiate.union(*self.headingdf.loc[start:end]['characters'])
    #         locationchar.append(intermidiate)
    #         for character in characterprescene:
    #             if character in intermidiate:
    #                 characterprescene[character].append(1)
    #             else:
    #                 characterprescene[character].append(0)
    #     locationdf['character'] = locationchar
    #     # locationdf
    #     characterpresecenedf = pd.DataFrame(characterprescene)
    #     alpha_character = list(self.characterdict.keys())
    #     alpha_character.sort()
    #
    #     self.locationdf = pd.concat([locationdf, pd.DataFrame(characterprescene, index=self.location_list)], axis=1)
    #
    #     self.locationcocurence = self.locationdf.copy()
    #     # self.locationcocurence.set_index('location', inplace=True)
    #     self.locationcocurence.drop(
    #         columns=['heading', 'terior', 'subheading', 'ToD', 'sentence_index', 'type', 'text', 'character'],
    #         inplace=True)


    def get_json_data(self):
        return self.screenplay,self.characterdict,self.location_list