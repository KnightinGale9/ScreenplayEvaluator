
import matplotlib.pyplot as plt
import numpy as np
import spacy
from CodeBase.GraphParent import GraphParent
# nlp = spacy.load("en_core_web_trf") #slow but more accurate
nlp = spacy.load("en_core_web_sm") #fast but less accurate
class IncreasingGraph(GraphParent):
    def increasing_graph(self):
        fig, ax = plt.subplots(figsize=(10, 5))

        for character in self.characterdict:
            xpoints = np.append([0], self.speaking[character])
            xpoints = np.append(xpoints, self.locationdf['sentence_index'].iloc[-1])
            ypoints = np.array(list(range(0, len(self.speaking[character]) + 1)))
            ypoints = np.append(ypoints, len(self.speaking[character]))
            plt.step(xpoints, ypoints, label=character, where='post', color=self.characterdict[character])

        plt.xticks(np.append([0], list(self.locationdf['sentence_index'])))
        plt.xlim([0, self.locationdf['sentence_index'].iloc[-1]])

        self.alt_bands(ax=ax)
        plt.xticks([])
        plt.savefig(self.filename.replace(".json", "-increasingGraph.png"))
        plt.close()
