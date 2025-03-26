from matplotlib import pyplot as plt

from CodeBase.Evaluator import Evaluator


class SentenceLengthByScene(Evaluator):
    """
    An evaluator that aggregates the length of the scene and visulize scene length over time and by index.

    Scene length, measured by the number of sentences, is a visual evaluation method for analyzing the number
    of sentences in each scene in a screenplay. This provides insight into the diversity and structural complexity of
    the screenplay.
    Attributes:
        differences:List of the length of each scene in the screenplay
    """
    def run_evaluator(self):
        self.create_scene_length()
        self.graph_over_time()
        self.graph_over_length()
        print("Sentence Length",end="")
    def create_scene_length(self):
        """
        Aggregates the length of the scene throughout hte screenplay.
        Initalizes self.differences
        """
        # print(self.scraper.get_locationlist())
        filtered_list = [x - 1 for x in self.scraper.get_locationlist() if x > 0]

        scenedf = self.scraper.get_fulldf()[self.scraper.get_fulldf().index.isin(filtered_list)]['sentence_index']
        # print(scenedf)
        scenelength=list(scenedf)
        scenelength.insert(0,0)
        # print("debug:",scenelength)
        self.differences = [scenelength[i + 1] - scenelength[i] for i in range(len(scenelength) - 1)]

    def graph_over_time(self):
        """
        Creates a scatter plot of scene length through the screenplay.
        X-axis denotes scene index. Y-axis denotes the scene length.
        :returns: None (Creates the file with the extension -SceneBySentenceLengthOverTime.png)
        """
        keys = [i for i in range(len(self.differences))]
        values = self.differences
        fig, ax = plt.subplots(figsize=(20, 10))

        plt.scatter(keys, values)
        plt.title("Scene By Sentence Length Over Time")

        ax.set_xlabel('Scene Index')
        ax.set_ylabel('Sentence Count')
        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-SceneBySentenceLengthOverTime.png")}',bbox_inches='tight')
        plt.close()
    def graph_over_length(self):
        """
        Creates a bar plot of scene length through the screenplay.
        X-axis denotes scene length. Y-axis denotes the count/index.
        :returns: None (Creates the file with the extension -SceneBySentenceLengthIndex.png)
        """
        self.scenelenlcolat = {}
        for x in self.differences:
            # print(x)
            if x not in self.scenelenlcolat:
                self.scenelenlcolat[x] = 0
            self.scenelenlcolat[x] += 1
        sorted_sentence = list(self.scenelenlcolat.items())
        sorted_sentence.sort()
        keys, values = zip(*sorted_sentence)
        fig, ax = plt.subplots(figsize=(20, 10))

        plt.bar(keys, values )
        plt.title("Scene By Sentence Length Index")
        ax.set_xlabel('Scene Length')
        ax.set_ylabel('Count')
        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-SceneBySentenceLengthIndex.png")}',bbox_inches='tight')
        plt.close()

    def get_json_data(self):
        """
        A function to retrieve the data created by sentence length by scene for Screenplay_Raw_data.json
        :return: self.scenelenlcolat,self.differences
        """
        return {"scenebysentence":self.scenelenlcolat,"scenelengthbysentence":self.differences}