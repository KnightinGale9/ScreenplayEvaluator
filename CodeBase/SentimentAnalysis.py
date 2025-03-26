import numpy as np
import pandas as pd
import spacy
from matplotlib import pyplot as plt
from transformers import pipeline

from CodeBase.GraphParent import GraphParent

#https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english#uses

class SentimentAnalysis(GraphParent):
    """
    An evaluator that calculates and visualizes Sentiment Analysis using a model from hugging face.

    Sentiment Analysis provides insights into the story’s emotional tone overall but can also help
    identify bias toward one sentiment over the other in the screenplay.
    Attributes:
        sentences: List of all sentences in the screenplay
        sentiement: List of sentiment value for all sentences in the screenplay
        positive: Dataframe of all the positive sentiment in the screenplay
        negative: Dataframe of all the negative sentiment in the screenplay
    """
    def run_evaluator(self):
        self.create_sentiment_list()
        self.create_graph()
        print("Sentiment Analysis",end="")
    def create_sentiment_list(self):
        """
        Calculates the sentiment analysis for each line of text.
        Initalizes self.sentences and self.sentiemnt
        """
        sentiment_pipeline = pipeline("sentiment-analysis",model="distilbert-base-uncased-finetuned-sst-2-english")

        self.sentences = []
        self.sentiemnt = []

        for text in self.scraper.get_sentences():
            self.sentences.append(text)
            self.sentiemnt.append(sentiment_pipeline(text))

    def create_graph(self):
        """
        Creates a scatter plot of sentiment scores for each sentence in the dataset.
        Positive sentiments are represented with green dots, and negative sentiments are represented
        with red dots. The sentiment score is plotted on the y-axis, and the sentence index on the x-axis.
        :returns: None (Creates the file with the extension -SentimentAnlysis.png)
        """
        values = []
        for outbar in self.sentiemnt:
            if outbar[0]['label'] == 'POSITIVE':
                values.append(outbar[0]['score'])
            else:
                values.append(outbar[0]['score'] * -1)
        # Plot the bar graph
        sentiment = pd.DataFrame({'sentences': self.sentences, 'sentiment_score': values})
        # print(sentiment)
        fig, ax = plt.subplots(figsize=(20, 10))

        # Separate positive and negative sentiment scores
        self.positive = sentiment[sentiment['sentiment_score'] >= 0]
        self.negative = sentiment[sentiment['sentiment_score'] < 0]

        # Plot positive sentiment scores as green bars
        bars_positive = ax.scatter(self.positive.index, self.positive['sentiment_score'], color='green', label='Positive')


        # Plot negative sentiment scores as red bars
        bars_negative = ax.scatter(self.negative.index, self.negative['sentiment_score'], color='red', label='Negative')

        # Add labels and title
        plt.legend()
        plt.xticks(np.append([0], list(self.scraper.get_locationdf()['sentence_index'])))
        plt.xlim([0, self.scraper.get_locationdf()['sentence_index'].iloc[-1]])

        self.x_axis_alt_bands(ax=ax)
        plt.xticks(list(range(0, list(self.scraper.get_locationdf()['sentence_index'])[-1], 500)))
        ax.set_xlabel('Sentence Index ')
        ax.set_ylabel('Sentiment Score')
        ax.set_title('Sentiment Analysis')
        plt.title("Sentiment score Over Sentence Index")

        plt.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension("-SentimentAnlysis.png")}',bbox_inches='tight')
        plt.close()

    def get_json_data(self):
        """
        A function to retrieve the data created by sentiment analysis for Screenplay_Raw_data.json
        :return: {"Pos_sentiment":len(self.positive),"Neg_sentiment":len(self.negative)},self.sentiemnt
        """
        return {"sentiment_percent":{"Pos_sentiment":len(self.positive),"Neg_sentiment":len(self.negative)},"sentiment":self.sentiemnt}