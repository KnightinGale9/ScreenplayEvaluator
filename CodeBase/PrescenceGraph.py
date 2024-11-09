from CodeBase.GraphParent import GraphParent
import matplotlib.pyplot as plt
import numpy as np

class PrescenceGraph(GraphParent):
    def prescence_graph(self):
        self.sorted_character = self.sorted_character_cocurancesum()

        # Sample data for events
        char = []
        events = []
        color = []
        for character in self.sorted_character:
            char.append(character)
            events.append(self.speaking[character])
            color.append(self.scraper.get_characterdict()[character])

        # Create figure and axis
        fig, ax = plt.subplots()
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
        # ax
        # ax.minorticks_on()
        # ax.grid(False)
        # # Adding legend manually
        plt.xticks(rotation=90)
        # plt.show()
        fig.tight_layout()

        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-prescenceGraph.png")}')
        plt.close()
