from CodeBase.GraphParent import GraphParent
import matplotlib.pyplot as plt
import numpy as np

class PrescenceGraph(GraphParent):
    """
    An evaluator that visualizes character presence using a presence graph.

    The Presence Graph is a visualizes a comprehensive overview of character involvement and appearance in the story,
     clearly highlighting when characters are present and when they share screen time with others.
    Attributes:
        sorted_character: List of the character sorted
    """
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
