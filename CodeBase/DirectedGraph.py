import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import PchipInterpolator

from CodeBase.Evaluator import Evaluator


class DirectedGraph(Evaluator):
    """
    An evaluator that generates and visulizes a Forced Directed Graph.

    A forced-directed graph is a representation of the character’s movement through the screenplay.
    This type of visualization provides valuable insights into how the writer organizes characters
    and scenes spatially and temporally within the story.
    Attributes:
        loc_graph: dictionary which stores that stores unique scene headings and give them an incremental number
        char_forced_directed: Stores each character appearance in each scene throughout the screenplay
    """
    def create_directed_graph(self):
        """
        Creates the data points for a directed graph of characters' appearances in scenes.
        Initalizes loc_graph and char_forced_directed
        """
        self.loc_graph = {}
        i = 0
        for loc in self.scraper.get_locationdf()["heading"]:
            if loc not in self.loc_graph:
                self.loc_graph[loc] = i
                i += 10

        self.char_forced_directed = {}
        for char in self.scraper.get_characterdict():
            self.char_forced_directed[char] = {"x_val": [], "y_val": []}
        last_heading = ""
        for idx, row in self.scraper.get_locationdf().iterrows():
            if last_heading == row['heading']:
                # print(last_heading,row)
                continue
            # print(idx,row['character'])
            char_scene = len(row['character'])
            for offset, charac in enumerate(row['character']):
                if len(self.char_forced_directed[charac]["x_val"]) != 0\
                        and idx - self.char_forced_directed[charac]["x_val"][-1] > 300:
                    self.char_forced_directed[charac]["x_val"].append(np.nan)
                    self.char_forced_directed[charac]["y_val"].append(np.nan)

                self.char_forced_directed[charac]["x_val"].append(row['sentence_index'])
                self.char_forced_directed[charac]["y_val"].append(
                    self.loc_graph[row['heading']] + offset * 10 / char_scene)
            last_heading = row['heading']

    def creategraph(self):
        """
        Creates a line graph for each character overlayed ontop of each other with an offset to create
        the forced directed graph. X-axis denotes the sentence index and the y-axis denotes the scene.
        :returns: None (Creates the file with the extension -DirectedGraph.png)
        """
        fig, ax = plt.subplots(figsize=(15, 20))
        fig.tight_layout()
        for character in self.scraper.get_characterdict():
            if np.nan in  self.char_forced_directed[character]["x_val"] or len(self.char_forced_directed[character]["x_val"])<2:
                plt.plot(self.char_forced_directed[character]["x_val"], self.char_forced_directed[character]["y_val"], marker='o',
                         color=self.scraper.get_characterdict()[character], label='Interpolated Points')  # Line plot with markers
            else:
                # print(char_forced_directed[character]["x_val"])
                pchip_interp = PchipInterpolator(self.char_forced_directed[character]["x_val"], self.char_forced_directed[character]["y_val"])

                # Generate new x values for smooth curve
                x_new = np.linspace(min(self.char_forced_directed[character]["x_val"]), max(
                    self.char_forced_directed[character]["x_val"]), 500)  # 500 points between the min and max of x
                y_new = pchip_interp(x_new)

                # Plot original points and interpolated curve
                plt.plot(self.char_forced_directed[character]["x_val"], self.char_forced_directed[character]["y_val"], marker='o',
                         color=self.scraper.get_characterdict()[character],label='Original Points')  # Original points
                plt.plot(x_new, y_new, '-', label='Cubic Interpolation')  # Interpolated curve
        yy = list(range(0, len(self.loc_graph) * 10, 10))
        yylabel = [val for val in self.loc_graph.keys()]

        plt.yticks(yy, yylabel)
        ax.grid(True, which='major', linestyle='--', linewidth=0.5, color='gray')
        plt.title("Forced Directed Graph")
        ax.set_xlabel('Sentence Index')
        ax.set_ylabel('Scene')

        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-DirectedGraph.png")}',bbox_inches='tight')
        plt.close()
