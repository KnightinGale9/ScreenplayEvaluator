from matplotlib import pyplot as plt

from CodeBase.Evaluator import Evaluator


class SceneLength(Evaluator):
    def create_scene_length(self):
        print(self.scraper.get_locationlist())
        filtered_list = [x - 1 for x in self.scraper.get_locationlist() if x > 0]

        scenedf = self.scraper.get_fulldf()[self.scraper.get_fulldf().index.isin(filtered_list)]['sentence_index']
        print(scenedf)
        scenelength=list(scenedf)
        scenelength.insert(0,0)
        print("debug:",scenelength)
        self.differences = [scenelength[i + 1] - scenelength[i] for i in range(len(scenelength) - 1)]

    def graph_over_time(self):
        keys = [i for i in range(len(self.differences))]
        values = self.differences
        plt.bar(keys, values )
        plt.savefig(self.scraper.get_filename().replace(".json", "-SceneLengthOverTime.png"))
        plt.close()
    def graph_over_length(self):
        self.scenellcolat = {}
        for x in self.differences:
            # print(x)
            if x not in self.scenellcolat:
                self.scenellcolat[x] = 0
            self.scenellcolat[x] += 1
        sorted_sentence = list(self.scenellcolat.items())
        sorted_sentence.sort()
        keys, values = zip(*sorted_sentence)
        plt.bar(keys, values, )
        plt.savefig(self.scraper.get_filename().replace(".json", "-SceneLengthIndex.png"))
        plt.close()
