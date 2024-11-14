from matplotlib import pyplot as plt

from CodeBase.Evaluator import Evaluator


class SentenceLengthByScene(Evaluator):
    def create_scene_length(self):
        # print(self.scraper.get_locationlist())
        filtered_list = [x - 1 for x in self.scraper.get_locationlist() if x > 0]

        scenedf = self.scraper.get_fulldf()[self.scraper.get_fulldf().index.isin(filtered_list)]['sentence_index']
        # print(scenedf)
        scenelength=list(scenedf)
        scenelength.insert(0,0)
        # print("debug:",scenelength)
        self.differences = [scenelength[i + 1] - scenelength[i] for i in range(len(scenelength) - 1)]

    def graph_over_time(self):
        keys = [i for i in range(len(self.differences))]
        values = self.differences
        fig, ax = plt.subplots(figsize=(10, 5))

        plt.bar(keys, values)
        plt.title("Scene By Sentence Length Over Time")

        ax.set_xlabel('Scene Index')
        ax.set_ylabel('Sentence Count')
        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-SceneBySentenceLengthOverTime.png")}')
        plt.close()
    def graph_over_length(self):
        self.scenelenlcolat = {}
        for x in self.differences:
            # print(x)
            if x not in self.scenelenlcolat:
                self.scenelenlcolat[x] = 0
            self.scenelenlcolat[x] += 1
        sorted_sentence = list(self.scenelenlcolat.items())
        sorted_sentence.sort()
        keys, values = zip(*sorted_sentence)
        fig, ax = plt.subplots(figsize=(10, 5))

        plt.bar(keys, values )
        plt.title("Scene By Sentence Length Index")
        ax.set_xlabel('Scene Length')
        ax.set_ylabel('Count')
        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-SceneBySentenceLengthIndex.png")}')
        plt.close()

    def get_json_data(self):
        return self.scenelenlcolat,self.differences