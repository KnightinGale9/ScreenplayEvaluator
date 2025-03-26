import matplotlib.pyplot as plt
import numpy as np

from CodeBase.Evaluator import Evaluator


class GraphParent(Evaluator):
    """
    A child of evaluator class that is intended to be inherited by evaluators that use graphs that need
    alternating bands. The class provides basic functionality for creating alternating bands on graphs.
    """
    def __init__(self, scraper):
        super().__init__(scraper=scraper)

    def x_axis_alt_bands(self,ax=None):
        """
        Adding alternating gray bands in the vertical for graphs such as increasing to denote scene changes
        :param ax:
        :return: None ( Gives the graph a alternating band in the x_axis)
        """
        ax = ax or plt.gca()
        x_left, x_right = ax.get_xlim()
        locs = ax.get_xticks()
        for loc1, loc2 in zip(locs[::2], np.concatenate((locs, [x_right]))[1::2]):
            ax.axvspan(loc1, loc2, facecolor='black', alpha=0.2)
        ax.set_xlim(x_left, x_right)

    def y_axis_alt_bands(self, ax=None):
        """
        Adding alternating gray bands in the horizontal for graphs such as presence to denote scene changes
        :param ax:
        :return: None ( Gives the graph a alternating band in the y_axis)
        """
        ax = ax or plt.gca()
        y_bottom, y_top = ax.get_ylim()
        locs = ax.get_yticks()
        for loc1, loc2 in zip(locs[::2], np.concatenate((locs, [y_top]))[1::2]):
            ax.axhspan(loc1, loc2, facecolor='black', alpha=0.2)
        ax.set_ylim(y_bottom, y_top)

    def heading_only_lines(self):
        """
        Retrieves only heading lines for presence and increasing graph
        :returns None (initalizes speaking)
        """
        self.speaking = {}

        for character in self.scraper.get_characterdict():
            self.speaking[character] = \
            self.scraper.get_dialoguedf().loc[self.scraper.get_dialoguedf()['type'] == character]['sentence_index']

    def character_dialogue_lines(self):
        """
        Retrieves only dialogue lines for presence and increasing graph
        :returns None (initalizes speaking)
        """
        self.speaking = {}

        for character in self.scraper.get_characterdict():
            self.speaking[character] = \
            self.scraper.get_headingdf()[self.scraper.get_headingdf()['characters'].apply(lambda x: character in x)][
                'sentence_index']

    def combined_lines(self):
        """
        Retrieves all lines for presence and increasing graph
        :returns None (initalizes speaking)
        """
        self.speaking = {}

        for character in self.scraper.get_characterdict():
            dia = set(
                self.scraper.get_dialoguedf().loc[self.scraper.get_dialoguedf()['type'] == character]['sentence_index'])
            setting = set(
                self.scraper.get_headingdf()[
                    self.scraper.get_headingdf()['characters'].apply(lambda x: character in x)]['sentence_index'])
            combine = list(dia.union(setting))
            combine.sort()
            self.speaking[character] = combine