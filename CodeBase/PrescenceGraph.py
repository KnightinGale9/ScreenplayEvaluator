from CodeBase.GraphParent import GraphParent
import matplotlib.pyplot as plt
import numpy as np
import spacy

# nlp = spacy.load("en_core_web_trf") #slow but more accurate
nlp = spacy.load("en_core_web_sm")  # fast but less accurate


class PrescenceGraph(GraphParent):
    def set_sorted_character(self, type):
        if type == "name":
            self.sorted_character = self.sorted_character_name()
        elif type == "size":
            self.sorted_character = self.sorted_character_length()
        elif type == "matrix":
            self.sorted_character = self.sorted_character_matrix()
        elif type == "cocurancesum":
            self.sorted_character = self.sorted_character_cocurancesum()
        else:
            self.sorted_character = self.scraper.get_characterdict()

    def prescence_graph(self):
        # Sample data for events
        char = []
        events = []
        color = []
        for character in self.sorted_character:
            char.append(character)
            events.append(self.speaking[character])
            color.append(self.scraper.get_characterdict()[character])

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plotting the event plot
        ax.eventplot(events, orientation='vertical', lineoffsets=range(0, len(self.speaking)), linelengths=0.7,
                     colors=color)

        ax.set_xticks(range(0, len(self.speaking)))
        ax.set_yticks((np.array(self.scraper.get_locationdf()['sentence_index'])))
        self.y_axis_alt_bands(ax=ax)
        ax.set_xticklabels(char)
        plt.margins(0)
        plt.yticks([])

        ax.set_xlabel('Character')
        ax.set_title('Presence Graph')
        # ax
        # ax.minorticks_on()
        # ax.grid(False)
        # # Adding legend manually
        ax.legend(loc='upper right')
        plt.xticks(rotation=90)
        # plt.show()
        plt.savefig(self.scraper.get_filename().replace(".json", "-prescenceGraph.png"))
        plt.close()
