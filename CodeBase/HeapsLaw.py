import re
from collections import defaultdict
import matplotlib.pyplot as plt

from CodeBase.Evaluator import Evaluator


class HeapsLaw(Evaluator):

    def heaps_law(self):
        vocabulary = defaultdict(int)
        self.vocab_growth = []
        i=0
        for _,row in self.scraper.get_fulldf().iterrows():
            # print(row['text'])
            for tt in row['text']:
                vocabulary[tt] += 1
                # Calculate expected vocab size according to Heap's law
                self.vocab_growth.append((i + 1, len(vocabulary)))
                i+=1
        return self.vocab_growth

    def plot_vocab_growth(self):
        """
        Plots the actual vocabulary growth vs. predicted growth from Heap's Law.

        :param vocab_growth: List of tuples (N, actual_vocab_size, predicted_vocab_size).
        """
        N = [point[0] for point in self.vocab_growth]
        actual_vocab_size = [point[1] for point in self.vocab_growth]
        # predicted_vocab_size = [point[2] for point in self.vocab_growth]

        fig, ax = plt.subplots()
        plt.plot(N, actual_vocab_size, label='Actual Vocabulary Size')
        plt.xlabel('Total Number of Words (N)')
        plt.ylabel('Vocabulary Size (V(N))')
        plt.title('Heap\'s Law: Vocabulary Growth')
        plt.yticks([0,25,50,75,100,125,150,175,200])
        plt.minorticks_on()

        # plt.legend()
        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension("-HeapsLaw.png")}',bbox_inches='tight')
        plt.close()

    def get_json_data(self):
        return self.vocab_growth
