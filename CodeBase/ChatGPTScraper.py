import json
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
            with open(file_path, 'r') as file:
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
        sent_idx = 0
        location = ""
        story_combine = ""
        pattern1 = r"(INT\.|EXT\.|I\/E\.|INT./EXT.)\s+(.*)\s+-\s+(.*)\s*"
        pattern2 = r"(INT\.|EXT\.|I\/E\.)\s+([A-Za-z\s]+?)\s+-\s+([A-Za-z\s]+)?\s+-\s+([A-Za-z]*)\s*"
        screen = self.data.split("\n\n")

        for text in screen:
            i = len(self.screenplay['type'])

            # print(i,text)
            # if "FADE" in text:
            #     print(text)
            #     continue
            if "EXT." in text or "INT." in text:
                location = text
                print(i, text)
                self.location_list.append(i)
                continue
            character = text.split("\n")
            if character[0].isupper():
                self.screenplay["type"].append(character[0])
                temp = ""
                for tt in character[1:]:
                    temp += tt
                self.screenplay["text"].append(temp)

            else:
                self.screenplay["type"].append("HEADING")
                self.screenplay["text"].append(text)

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
                print(location)
                print("error", text)
            # screenplay["location"].append(location)
            sent_idx += self.count_sentences(text)
            self.screenplay["sentence_index"].append(sent_idx)

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

