import re
from collections import defaultdict
import matplotlib.pyplot as plt

from CodeBase.Evaluator import Evaluator


class HeapsLaw(Evaluator):

    def heaps_law(self,k=10, beta=0.5):
        vocabulary = defaultdict(int)
        self.vocab_growth = []

        for i,row in self.scraper.get_fulldf().iterrows():
            # print(row['text'])
            for tt in row['text']:
                vocabulary[tt] += 1
                # Calculate expected vocab size according to Heap's law
                predicted_vocab_size = k * (i + 1) ** beta
                self.vocab_growth.append((i + 1, len(vocabulary), predicted_vocab_size))
        return self.vocab_growth

    def plot_vocab_growth(self):
        """
        Plots the actual vocabulary growth vs. predicted growth from Heap's Law.

        :param vocab_growth: List of tuples (N, actual_vocab_size, predicted_vocab_size).
        """
        N = [point[0] for point in self.vocab_growth]
        actual_vocab_size = [point[1] for point in self.vocab_growth]
        predicted_vocab_size = [point[2] for point in self.vocab_growth]

        plt.figure(figsize=(10, 6))
        plt.plot(N, actual_vocab_size, label='Actual Vocabulary Size')
        plt.plot(N, predicted_vocab_size, label='Predicted Vocabulary Size (Heap\'s Law)', linestyle='--')
        plt.xlabel('Total Number of Words (N)')
        plt.ylabel('Vocabulary Size (V(N))')
        plt.title('Heap\'s Law: Vocabulary Growth')
        plt.yticks([0,50,100,150,200,250,300])
        plt.legend()
        plt.savefig(f'../output/{self.scraper.get_filename().replace(".json", "-HeapsLaw.png")}')
        plt.close()

    def get_json_data(self):
        return self.vocab_growth
