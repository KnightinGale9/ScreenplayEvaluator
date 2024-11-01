import json
import pandas as pd
import spacy
import seaborn as sns
import colorcet as cc

from CodeBase.Scraper import Scraper

# nlp = spacy.load("en_core_web_trf") #slow but more accurate
nlp = spacy.load("en_core_web_sm") #fast but less accurate


class ScreenPyScrapper(Scraper):
    def __init__(self,file_path):
        try:
            f = open(file_path)
            self.data = json.load(f)
            self.filename=file_path
            f.close()
        except FileNotFoundError:
            print(file_path+ " was not found.")
    def screenplay_scrape(self):
        self.screenplay = {'sentence_index': [], 'type': [], 'location': [], 'text': []}
        basic = {'ToD': None, 'shot type': None, 'location': None, 'terior': None, 'subj': None}
        self.location_list = []
        i = 0
        sent_idx = 0
        for scene in self.data:
            location = scene[0]["head_text"]
            self.location_list.append(i)
            # print(i,location)
            for screen in scene:
                if screen["head_type"] == 'heading':
                    if screen['head_text']['subj'] == 'FADE IN':
                        #                 print(screen)
                        continue
                    self.screenplay['type'].append(screen["head_type"].upper())
                    # print(screen['head_text'])
                    if screen['head_text'] != location and screen['head_text']['terior'] is not None:
                        # print(i,location)
                        location = screen['head_text']
                        self.location_list['index'].append(i)

                elif screen["head_type"] == 'speaker/title':
                    self.screenplay['type'].append(screen["head_text"]['speaker/title'].split('(')[0].strip())
                else:
                    continue
                process_text = str(screen['text'].strip())
                split_text = process_text.split(".")
                while "" in split_text:
                    split_text.remove("")
                sent_idx += len(split_text)
                self.screenplay['sentence_index'].append(sent_idx)
                self.screenplay['text'].append(process_text)
                screenplayTXT = f"{location['terior']} {location['location']} "
                if location['subj'] is not None:
                    screenplayTXT += f" {location['subj']}"
                if location['ToD'] is not None:
                    screenplayTXT += f"- {location['ToD']}"
                self.screenplay['location'].append(screenplayTXT)

                # screenplay['text'].append(nlp(screen['text']))
                i += 1
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
        print(self.fulldf)
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
            intermidiate=set(
                self.fulldf.loc[self.fulldf['location'] == loca]['type'])
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


