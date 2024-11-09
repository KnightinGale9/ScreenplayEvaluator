import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import linkage, leaves_list

from CodeBase.Evaluator import Evaluator


class GraphParent(Evaluator):
    def __init__(self, scraper):
        super().__init__(scraper=scraper)

    def x_axis_alt_bands(self,ax=None):
        ax = ax or plt.gca()
        x_left, x_right = ax.get_xlim()
        locs = ax.get_xticks()
        for loc1, loc2 in zip(locs[::2], np.concatenate((locs, [x_right]))[1::2]):
            ax.axvspan(loc1, loc2, facecolor='black', alpha=0.2)
        ax.set_xlim(x_left, x_right)

    def y_axis_alt_bands(self, ax=None):
        ax = ax or plt.gca()
        y_bottom, y_top = ax.get_ylim()
        locs = ax.get_yticks()
        for loc1, loc2 in zip(locs[::2], np.concatenate((locs, [y_top]))[1::2]):
            ax.axhspan(loc1, loc2, facecolor='black', alpha=0.2)
        ax.set_ylim(y_bottom, y_top)

    def heading_only_lines(self):
        self.speaking = {}

        for character in self.scraper.get_characterdict():
            self.speaking[character] = self.scraper.get_dialoguedf().loc[self.scraper.get_dialoguedf()['type'] == character]['sentence_index']

    def character_dialogue_lines(self):
        self.speaking = {}

        for character in self.scraper.get_characterdict():
            self.speaking[character] = self.scraper.get_headingdf()[self.scraper.get_headingdf()['characters'].apply(lambda x: character in x)][
                'sentence_index']

    def combined_lines(self):
        self.speaking = {}

        for character in self.scraper.get_characterdict():
            dia = set(self.scraper.get_dialoguedf().loc[self.scraper.get_dialoguedf()['type'] == character]['sentence_index'])
            setting = set(
                self.scraper.get_headingdf()[self.scraper.get_headingdf()['characters'].apply(lambda x: character in x)]['sentence_index'])
            combine = list(dia.union(setting))
            combine.sort()
            self.speaking[character] = combine

    def sorted_character_name(self):

        sorted_character = list(self.speaking.items())
        sorted_character.sort()
        # print(sorted_character)
        sorted_character = [k for k, v in sorted_character]
        # print(sorted_character)
        return sorted_character

    def sorted_character_length(self):
        sorted_character = list(self.speaking.items())
        sorted_character.sort()
        sorted_character = sorted(sorted_character, key=lambda x: len(x[1]), reverse=True)
        print(sorted_character)
        sorted_character = [k for k, v in sorted_character]

        return sorted_character

    def sorted_character_matrix(self):
        co_occurrence = np.dot(self.scraper.get_locationcocurence().T, self.scraper.get_locationcocurence())
        linkage_matrix = linkage(co_occurrence, method='single')
        dendrogram_order = leaves_list(linkage_matrix)

        # Reorder characters
        characters = self.scraper.get_locationcocurence().columns
        reordered_characters = characters[dendrogram_order]

        # Reorder data for plotting
        sorted_character = self.scraper.get_locationcocurence()[reordered_characters]
        return sorted_character

    def sorted_character_cocurancesum(self):
        co_occurrence = np.dot(self.scraper.get_locationcocurence().T, self.scraper.get_locationcocurence())
        co_occurrence_sums = co_occurrence.sum(axis=1)

        # Sort characters based on their co-occurrence sums
        sorted_indices = np.argsort(co_occurrence_sums)[::-1]
        sorted_character = self.scraper.get_locationcocurence().columns[sorted_indices]
        return sorted_character