from CodeBase.GraphParent import GraphParent
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import linkage, leaves_list

class PrescenceGraph(GraphParent):
    """
    An evaluator that visualizes character presence using a presence graph.

    The Presence Graph is a visualizes a comprehensive overview of character involvement and appearance in the story,
     clearly highlighting when characters are present and when they share screen time with others.
    Attributes:
        sorted_character: List of the character sorted
    """
    def run_evaluator(self):
        self.combined_lines()
        self.prescence_graph()
        print("Presence Graph",end="")
    def prescence_graph(self):
        """
        Generates the data points for presence graph and graphs the data points .
        Creates a event plot of character appearence to denote the increasing graph.
        The x-axis denotes the character while the y axis denotes the character activity throughout the scene.
        :return: None (Creates the file with the extension -prescenceGraph.png).
        """
        self.sorted_character = self.sorted_character_cocurancesum()

        # Sample data for events
        char = []
        events = []
        color = []
        for character in self.sorted_character:
            cc= character.split()
            if len(cc)>3:
                char.append(f'{cc[0]} {cc[1]}')
            else:
                char.append(character)
            events.append(self.speaking[character])
            color.append(self.scraper.get_characterdict()[character])

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(20, 10))
        # Plotting the event plot
        ax.eventplot(events, orientation='vertical', lineoffsets=range(0, len(self.speaking)), linelengths=0.7,
                     colors=color)

        ax.set_xticks(range(0, len(self.speaking)))
        ax.set_yticks((np.array(self.scraper.get_locationdf()['sentence_index'])))
        self.y_axis_alt_bands(ax=ax)
        ax.set_xticklabels(char)
        plt.margins(0)
        plt.yticks(list(range(0,list(self.scraper.get_locationdf()['sentence_index'])[-1], 500)))

        ax.set_ylabel('Sentence Index')
        ax.set_title('Presence Graph')

        plt.xticks(rotation=90,fontsize=8)
        fig.tight_layout()

        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-prescenceGraph.png")}',bbox_inches='tight')
        plt.close()

    def get_json_data(self):
        """
        A function to retrieve the data created by increasing graph for Screenplay_Raw_data.json
        :return: speaking
        """
        return {"speaking": self.speaking}
    def sorted_character_name(self):
        """
        Sorts the character dictionary key by sorting by name.
        :return: sorted_character
        """
        sorted_character = list(self.speaking.items())
        sorted_character.sort()
        # print(sorted_character)
        sorted_character = [k for k, v in sorted_character]
        # print(sorted_character)
        return sorted_character

    def sorted_character_length(self):
        """
        Sorts the character dictionary key by sorting by character activity in the story.
        :return: sorted_character
        """
        sorted_character = list(self.speaking.items())
        sorted_character.sort()
        sorted_character = sorted(sorted_character, key=lambda x: len(x[1]), reverse=True)
        print(sorted_character)
        sorted_character = [k for k, v in sorted_character]

        return sorted_character

    def sorted_character_matrix(self):
        """
        Sorts the character dictionary key by sorting by linkage_matrix.
        :return: sorted_character
        """
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
        """
        Sorts the character dictionary key by sorting by coocurance sum
        :return: sorted_character
        """
        co_occurrence = np.dot(self.scraper.get_locationcocurence().T, self.scraper.get_locationcocurence())
        co_occurrence_sums = co_occurrence.sum(axis=1)

        # Sort characters based on their co-occurrence sums
        sorted_indices = np.argsort(co_occurrence_sums)[::-1]
        sorted_character = self.scraper.get_locationcocurence().columns[sorted_indices]
        return sorted_character