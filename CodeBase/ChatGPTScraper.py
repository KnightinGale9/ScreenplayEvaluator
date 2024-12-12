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


class ChatGPTScraper(Scraper):
    def __init__(self,dirpath,file_path):
        self.dir_path=dirpath
        try:
            with open(file_path, 'r',encoding="utf8") as file:
                self.data = file.read()
            self.filename=file_path
            match = re.search(r"\/(.*)$", file_path)
            if match:
                self.filename = match.group(1)  # Access group 1
                print(self.filename)
        except FileNotFoundError:
            print(file_path+ " was not found.")

    def screenplay_scrape(self):
        self.screenplay = {'sentence_index': [], 'type': [], 'terior': [], 'heading': [], 'subheading': [], 'ToD': [],
                      'text': []}
        self.location_list = []
        self.sentences=[]
        sent_idx = 0
        location = ""

        story_combine = ""
        pattern1 = r".*(INT\.|EXT\.|I\/E\.|INT\.\/EXT\.)\s+(.*)\s+[-—–]\s+(.*)\s*.*"
        pattern2 = r".*(INT\.|EXT\.|I\/E\.|INT\.\/EXT\.)\s+(.*)\s+[-—–]\s+(.*)\s+[-–]\s+(.*)\s*.*"
        screen = self.data.split("\n\n")

        for text in screen:
            i = len(self.screenplay['type'])

            # print(i,text)
            if "EXT." in text or "INT." in text:
                # if text != location:
                location = text.replace("\n","").strip()
                # print(i, text)
                self.location_list.append(i)
                continue
            trans=r"^\b(?:FADE IN|FADE OUT|DISSOLVE TO|CUT TO|SMASH CUT|IRIS IN AND IRIS OUT|JUMP CUT|FLASHBACK|TIME CUT|THE END.)\b.(.*)"
            if re.match(trans,text):
                mat = re.match(trans, text)
                print(text)
                if mat.group(1) is not None:
                    continue

            character = text.split("\n")
            if character[0].isupper():
                character_name = character[0].split("(")
                self.screenplay["type"].append(character_name[0].strip())
                temp = ""
                for tt in character[1:]:
                    temp += tt
                pharentetical = r'(\(.*?\))?\s*(.*)'
                mat = re.match(pharentetical, temp)
                self.screenplay["text"].append(mat.group(2))
                sent = nltk.sent_tokenize(mat.group(2))
                sent_idx += len(sent)
                self.sentences.extend(sent)
                self.screenplay["sentence_index"].append(sent_idx)

            else:
                self.screenplay["type"].append("HEADING")
                self.screenplay["text"].append(text)
                sent = nltk.sent_tokenize(text)
                sent_idx += len(sent)
                self.sentences.extend(sent)
                self.screenplay["sentence_index"].append(sent_idx)

            if re.match(pattern2, location):
                mat = re.match(pattern2, location)
                self.screenplay['terior'].append(mat.group(1))  # INT.
                self.screenplay['heading'].append(mat.group(2))  # ANCIENT CITY
                self.screenplay['subheading'].append(mat.group(3))  # UNDERGROUND PASSAGE
                self.screenplay['ToD'].append(mat.group(4))  # NIGHT
                # location_list.append(i)

            elif re.match(pattern1, location):
                mat = re.match(pattern1, location)
                self.screenplay['terior'].append(mat.group(1))  # INT.
                self.screenplay['heading'].append(mat.group(2))  # ANCIENT CITY
                self.screenplay['subheading'].append(None)  # UNDERGROUND PASSAGE
                self.screenplay['ToD'].append(mat.group(3))  # NIGHT
                # location_list.append(i)
            else:
                print(location,text)
                print("error")
            # screenplay["location"].append(location)
            # sent = nltk.sent_tokenize(text)
            # sent_idx += len(sent)
            # self.sentences.extend(sent)
            # self.screenplay["sentence_index"].append(sent_idx)
        temp = set(self.location_list)
        self.location_list = list(temp)
        self.location_list.sort()
        for ss in self.screenplay:
            print(len(self.screenplay[ss]))
    # def dataframe_creation(self,character_removal=[]):
    #
    #     self.fulldf = pd.DataFrame(self.screenplay)
    #     self.fulldf.drop(self.fulldf.loc[self.fulldf['text'] == ""].index, inplace=True)
    #     character_set = set(self.fulldf.loc[self.fulldf['type'] != "HEADING"]['type'])
    #     sorted_character = list(character_set)
    #     sorted_character.sort()
    #     sorted_character = [k for k in sorted_character]
    #     palette = sns.color_palette(cc.glasbey, n_colors=len(character_set))
    #     # character dict
    #     self.characterdict = dict(zip(sorted_character, palette))
    #     print(self.fulldf)
    #     self.dialoguedf = self.fulldf.loc[self.fulldf['type'] != "HEADING"]
    #
    #     self.headingdf = self.fulldf.loc[self.fulldf['type'] == "HEADING"]
    #     heading_character = []
    #
    #     characterset = set(self.characterdict.keys())
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
    #     # location df
    #     self.locationdf = self.fulldf[self.fulldf.index.isin(self.location_list)].copy()
    #
    #     # locationdf.loc[:, locationdf.columns != 'location']
    #     locationchar = []
    #     characterprescene = {key: [] for key in self.characterdict.keys()}
    #     for loca in self.locationdf['heading']:
    #         intermidiate = set(self.fulldf.loc[self.fulldf['heading'] == loca]['type'])
    #         intermidiate.union(*self.headingdf.loc[self.headingdf['heading'] == loca]['heading'])
    #         locationchar.append(intermidiate)
    #         for character in characterprescene:
    #             if character in intermidiate:
    #                 characterprescene[character].append(1)
    #             else:
    #                 characterprescene[character].append(0)
    #     self.locationdf['character'] = locationchar
    #     alpha_character = list(self.characterdict.keys())
    #     alpha_character.sort()
    #     self.locationdf
    #     for character in alpha_character:
    #         self.locationdf[character] = characterprescene[character]
    #
    #     self.locationcocurence = self.locationdf.copy()
    #     # self.locationcocurence.set_index('location', inplace=True)
    #     self.locationcocurence.drop(
    #         columns=['heading', 'terior', 'subheading', 'ToD', 'sentence_index', 'type', 'text', 'character'],
    #         inplace=True)

    def count_sentences(self,text):
        # Use regular expression to find sentences
        sentences = re.split(r'[.!?]+', text)

        # Filter out empty strings and count
        return len([s for s in sentences if s.strip()])

    def get_json_data(self):
        return self.screenplay,self.characterdict,self.location_list

