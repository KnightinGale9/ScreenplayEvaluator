from matplotlib import pyplot as plt
import regex as re

from CodeBase.Evaluator import Evaluator


class WordLengthByScene(Evaluator):
    def count_words_in_range(self,text):
        # Slice the string between the indice
        # print(text)
        substring = text
        # Split the substring by spaces and count the words
        word_count = len(substring.split())
        count = len(re.findall(r'\w+', text))

        return count
    def create_scene_length(self):
        self.wordcountlist = []
        wclist = self.scraper.get_locationlist()[1:].copy()
        wclist.append(len(self.scraper.get_fulldf()))
        for start, end in zip(self.scraper.get_locationlist()[1:], wclist):
            word_count = self.scraper.get_fulldf().loc[start:end]['text'].apply(lambda x: self.count_words_in_range(x))
            self.wordcountlist.append(int(word_count.sum()))

    def graph_over_time(self):
        keys = [i for i in range(len(self.wordcountlist))]
        values = self.wordcountlist
        fig, ax = plt.subplots(figsize=(10, 5))

        plt.bar(keys, values)
        plt.title("Scene Length Over Time")

        ax.set_xlabel('Scene Index')
        ax.set_ylabel('Sentence Count')
        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-SceneByWordLengthOverTime.png")}')
        plt.close()
    def graph_over_length(self):
        self.scenelenlcolat = {}
        for x in self.wordcountlist:
            # print(x)
            if x not in self.scenelenlcolat:
                self.scenelenlcolat[x] = 0
            self.scenelenlcolat[x] += 1
        sorted_sentence = list(self.scenelenlcolat.items())
        sorted_sentence.sort()
        keys, values = zip(*sorted_sentence)
        fig, ax = plt.subplots(figsize=(10, 5))

        plt.bar(keys, values )
        plt.title("Scene Length Index")
        ax.set_xlabel('Scene Length')
        ax.set_ylabel('Count')
        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-SceneByWordLengthIndex.png")}')
        plt.close()

    def get_json_data(self):
        return self.scenelenlcolat,self.wordcountlist