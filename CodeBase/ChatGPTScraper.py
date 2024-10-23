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
    def __init__(self,file_path):
        try:
            with open('example.txt', 'r') as file:
                self.data = file.read()
            self.filename=file_path
        except FileNotFoundError:
            print(file_path+ " was not found.")
    def screenplay_scrape(self):
        self.screenplay = {'sentence_index': [], 'type': [], 'location': [], 'text': []}
        location_list = []
        sent_idx = 0
        location = ""
        story_combine = ""
        screen = self.data.split("\n\n")

        for i, text in enumerate(screen):
            # print(i,text)
            if "EXT." in text or "INT." in text:
                location = text
                print(i, text)
                location_list.append(i)
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

            self.screenplay["location"].append(location)
            sent_idx += self.count_sentences(text)
            self.screenplay["sentence_index"].append(sent_idx)

    def dataframe_creation(self,character_removal=[]):

        self.fulldf = pd.DataFrame(self.screenplay)
        self.fulldf.drop(self.fulldf.loc[self.fulldf['text'] == ""].index, inplace=True)
        character_set = set(self.fulldf.loc[self.fulldf['type'] != "HEADING"]['type'])
        sorted_character = list(character_set)
        sorted_character.sort()
        sorted_character = [k for k in sorted_character]
        palette = sns.color_palette(cc.glasbey, n_colors=len(character_set))
        #character dict
        self.characterdict = dict(zip(sorted_character, palette))
        for removal in character_removal:
            if removal in self.characterdict:
                self.characterdict.pop(removal)
                for idx, row in self.fulldf.loc[self.fulldf['type'] == removal].iterrows():
                    self.fulldf.loc[idx, "text"] = str(row['type'] + " " + row['text'])
                    self.fulldf.loc[idx, 'type'] = "HEADING"

        self.dialoguedf = self.fulldf.loc[self.fulldf['type'] != "HEADING"]

        self.headingdf = self.fulldf.loc[self.fulldf['type'] == "HEADING"]
        heading_character = []

        characterset = set(self.characterdict.keys())
        for idx, row in self.headingdf.iterrows():
            # print(idx,row['text'].upper())
            nlpset = set()
            # nlpset.add()
            # print(row['text'].upper())
            for token in nlp(row['text'].upper()):
                nlpset.add(token.lemma_.upper())
            heading_character.append(characterset.intersection(nlpset).copy())
            # if idx == 80:
            #     print(heading_character[-1], nlpset)
        self.headingdf = self.headingdf.assign(characters=heading_character)
        #location df
        self.locationdf = self.fulldf[self.fulldf.index.isin(self.location_list)].copy()

        # locationdf.loc[:, locationdf.columns != 'location']
        locationchar = []
        characterprescene = {key: [] for key in self.characterdict.keys()}
        for loca in self.locationdf['location']:
            intermidiate = set(self.fulldf.loc[self.fulldf['location'] == loca]['type']).difference(
                character_removal.union(set(["HEADING"])))
            intermidiate.union(*self.headingdf.loc[self.headingdf['location'] == loca]['characters'])
            locationchar.append(intermidiate)
            for character in characterprescene:
                if character in intermidiate:
                    characterprescene[character].append(1)
                else:
                    characterprescene[character].append(0)
        self.locationdf['character'] = locationchar
        alpha_character = list(self.characterdict.keys())
        alpha_character.sort()
        for character in alpha_character:
            self.locationdf[character] = characterprescene[character]

        self.locationcocurence = self.locationdf.copy()
        self.locationcocurence.set_index('location', inplace=True)
        self.locationcocurence.drop(columns=['sentence_index', 'type', 'text', 'character'], inplace=True)


    def count_sentences(self,text):
        # Use regular expression to find sentences
        sentences = re.split(r'[.!?]+', text)

        # Filter out empty strings and count
        return len([s for s in sentences if s.strip()])

