import pandas as pd
import spacy
import seaborn as sns
import colorcet as cc

# nlp = spacy.load("en_core_web_trf") #slow but more accurate
nlp = spacy.load("en_core_web_sm") #fast but less accurate

class Scraper(object):

    """
     Base class for processing scraped screenplay data (in the form of dictionary), ensuring it is properly
     formatted and split into necessary attributes for evaluators.

    This class extracts structured data from screenplays, processes it into
    DataFrames, and provides various methods for accessing formatted data.

    Attributes:
        fulldf : The dataframe containing the full screenplay
        characterdict : Dictionary containing all the characters of the screenplay
        dialoguedf : A subset dataframe of fulldf containing only dialogue
        headingdf : A subset dataframe of fulldf containing non dialogue lines
        locationdf : A subset of dataframe of fulldf containg only the first line of all scene
        location_list : A list containing all the indexes of locations in the screeenplay
        locationcocurence: A dataframe containing all scene and which character are present
                           to calculate co-occurrence relationship
    """

    def screenplay_scrape(self):
        """
        Method to be overwritten to scrape the specific data from screenplay and placed into a
        dictionary of self.screenplay = {'sentence_index': [], 'type': [], 'terior': [], 'heading': [],
         'subheading': [], 'ToD': [], 'text': []}
        """
        pass
    def dataframe_creation(self):
        """
        Taking the dictionary from scraper and converting the data into the proper dataframes for use in Evaluators.
        """
        self.fulldf = pd.DataFrame(self.screenplay)
        # self.fulldf.drop(self.fulldf.loc[self.fulldf['text'] == ""].index, inplace=True)
        character_set = set(self.fulldf.loc[self.fulldf['type'] != "HEADING"]['type'])
        sorted_character = list(character_set)
        sorted_character.sort()
        sorted_character = [k for k in sorted_character]
        palette = sns.color_palette(cc.glasbey, n_colors=len(character_set))
        #character dict
        self.characterdict = dict(zip(sorted_character, palette))
        if "" in self.characterdict:
            self.characterdict.pop("")
            for idx, row in self.fulldf.loc[self.fulldf['type'] == ""].iterrows():
                self.fulldf.loc[idx, "text"] = str(row['type'] + " " + row['text'])
                self.fulldf.loc[idx, 'type'] = "HEADING"
        # print(self.fulldf)
        self.dialoguedf = self.fulldf.loc[self.fulldf['type'] != "HEADING"].copy()

        self.headingdf = self.fulldf.loc[self.fulldf['type'] == "HEADING"].copy()
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

        locationdf = self.fulldf[self.fulldf.index.isin(self.location_list)].copy()

        # locationdf.loc[:, locationdf.columns != 'location']
        locationchar = []
        characterprescene = {key: [] for key in self.characterdict.keys()}
        wclist = self.location_list[1:].copy()
        wclist.append(len(self.fulldf))

        for start, end in zip(self.location_list, wclist):
            intermidiate = set(self.fulldf.loc[start:end]['type']).difference(set(["HEADING"]))
            intermidiate.union(*self.headingdf.loc[start:end]['characters'])
            locationchar.append(intermidiate)
            for character in characterprescene:
                if character in intermidiate:
                    characterprescene[character].append(1)
                else:
                    characterprescene[character].append(0)
        locationdf['character'] = locationchar
        # locationdf

        self.locationdf = pd.concat([locationdf, pd.DataFrame(characterprescene, index=self.location_list)], axis=1)
        # print(self.locationdf)

        self.locationcocurence = self.locationdf.copy()
        # self.locationcocurence.set_index('location', inplace=True)
        self.locationcocurence.drop(
            columns=['heading', 'character','terior', 'subheading', 'ToD', 'sentence_index', 'type', 'text'],
            inplace=True)
    def get_filename(self):
        return self.filename
    def get_fulldf(self):
        return self.fulldf
    def get_characterdict(self):
        return self.characterdict
    def get_headingdf(self):
        return self.headingdf
    def get_locationdf(self):
        return self.locationdf
    def get_dialoguedf(self):
        return self.dialoguedf
    def get_locationcocurence(self):
        return self.locationcocurence
    def get_locationlist(self):
        return self.location_list
    def get_sentences(self):
        return self.sentences
    def get_output_dir(self):
        return self.dir_path
