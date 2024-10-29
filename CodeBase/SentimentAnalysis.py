import pandas as pd
import spacy
from matplotlib import pyplot as plt
from transformers import pipeline

from CodeBase.Evaluator import Evaluator
nlp = spacy.load("en_core_web_sm") #fast but less accurate


class SentimentAnalysis(Evaluator):
    def create_sentiment_list(self):
        sentiment_pipeline = pipeline("sentiment-analysis")

        self.sentences = []
        self.sentiemnt = []
        for index, row in self.scraper.get_fulldf().iterrows():
            text = nlp(row['text'])
            span = list(text.sents)
            for txt in span:
                txt = txt
                if txt.text == "":
                    continue
                self.sentences.append(txt)
                self.sentiemnt.append(sentiment_pipeline(txt.text))

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
        fig, ax = plt.subplots(figsize=(20, 5))

        # Separate positive and negative sentiment scores
        positive = sentiment[sentiment['sentiment_score'] >= 0]
        negative = sentiment[sentiment['sentiment_score'] < 0]

        # Plot positive sentiment scores as green bars
        bars_positive = ax.bar(positive.index, positive['sentiment_score'], color='green', label='Positive')

        # Plot negative sentiment scores as red bars
        bars_negative = ax.bar(negative.index, negative['sentiment_score'], color='red', label='Negative')

        # Add labels and title
        ax.set_xlabel('ID')
        ax.set_ylabel('Sentiment Score')
        ax.set_title('Sentiment Analysis')
        # ax.legend()

        plt.savefig(self.scraper.get_filename().replace(".json", "-SentimentAnlysis.png"))
        plt.close()
        