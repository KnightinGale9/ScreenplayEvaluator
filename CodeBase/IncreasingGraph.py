
import matplotlib.pyplot as plt
import numpy as np
from CodeBase.GraphParent import GraphParent
class IncreasingGraph(GraphParent):
    def increasing_graph(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        for character in self.scraper.get_characterdict():
            xpoints = np.append([0], self.speaking[character])
            xpoints = np.append(xpoints, self.scraper.get_locationdf()['sentence_index'].iloc[-1])
            ypoints = np.array(list(range(0, len(self.speaking[character]) + 1)))
            ypoints = np.append(ypoints, len(self.speaking[character]))
            plt.step(xpoints, ypoints, label=character, where='post', color=self.scraper.get_characterdict()[character])

        plt.xticks(np.append([0], list(self.scraper.get_locationdf()['sentence_index'])))
        plt.xlim([0, self.scraper.get_locationdf()['sentence_index'].iloc[-1]])

        self.x_axis_alt_bands(ax=ax)
        plt.xticks(list(range(0,list(self.scraper.get_locationdf()['sentence_index'])[-1], 500)))
        plt.title("Increasing Graph ")
        ax.set_xlabel('Sentence Index')
        ax.set_ylabel('Character Presence ')
        # plt.legend(ncol=3)
        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-increasingGraph.png")}')
        plt.close()
    def get_json_data(self):
        return self.speaking