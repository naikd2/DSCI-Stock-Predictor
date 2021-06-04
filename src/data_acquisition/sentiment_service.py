from nltk.sentiment import SentimentIntensityAnalyzer
import operator

class SentimentService:

    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def assign(self, text):
        score = self.sia.polarity_scores(text)
        score.pop('compound')
        return max(score.items(), key=operator.itemgetter(1))[0]
