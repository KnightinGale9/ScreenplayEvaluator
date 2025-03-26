import re
from collections import defaultdict
import matplotlib.pyplot as plt

from CodeBase.Evaluator import Evaluator


class HeapsLaw(Evaluator):
    """
    An evaluator that calculates and visualizes vocabulary growth according to Heap's Law.

    Heap's Law describes the relationship between the total number of words (N) and the
    vocabulary size (V(N)) in a corpus of text.
    Attributes:
        vocab_growth: A list holding the word index and vocabulary size.
    """
    def run_evaluator(self):
        self.heaps_law()
        self.plot_vocab_growth()
        print("Heaps Law",end="")
    def heaps_law(self):
        """
        Calculates the actual vocabulary growth in the text, based on Heap's Law.
        :return: A list of tuples, where each tuple is (i, vocab_size), where 'i' is the number
                 of words processed and 'vocab_size' is the number of unique words encountered.
        """
        vocabulary = defaultdict(int)
        self.vocab_growth = []
        i=0
        for _,row in self.scraper.get_fulldf().iterrows():
            for tt in row['text']:
                vocabulary[tt] += 1
                # Calculate expected vocab size according to Heap's law
                self.vocab_growth.append((i + 1, len(vocabulary)))
                i+=1
        return self.vocab_growth

    def plot_vocab_growth(self):
        """
        Creates a line plot showing the vocabulary growth over the screenplay.
        The x axis denotes the sentence index while the y axis denotes the vocabulary size
        :return: None. (Creates the file with the extension -HeapsLaw.png)
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
        """
        Returns the evaluation data in a JSON-compatible format for the file Screenplay_Raw_data.json.

        :return: vocab_growth.
        """
        return {"vocabGrowth":self.vocab_growth}
