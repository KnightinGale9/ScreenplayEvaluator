import numpy as np
import pandas as pd
import spacy
from matplotlib import pyplot as plt
from transformers import pipeline

from CodeBase.Evaluator import Evaluator
from CodeBase.GraphParent import GraphParent

nlp = spacy.load("en_core_web_sm") #fast but less accurate

#https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english#uses

class SentimentAnalysis(GraphParent):
    def create_sentiment_list(self):
        sentiment_pipeline = pipeline("sentiment-analysis",model="distilbert-base-uncased-finetuned-sst-2-english")

        self.sentences = []
        self.sentiemnt = []

        for text in self.scraper.get_sentences():
            self.sentences.append(text)
            self.sentiemnt.append(sentiment_pipeline(text))

    def create_graph(self):
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
        return {"Pos_sentiment":len(self.positive),"Neg_sentiment":len(self.negative)},self.sentiemnt