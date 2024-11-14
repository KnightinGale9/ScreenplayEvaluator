import sys
import json

from CodeBase.Evaluator import Evaluator

try:
    from nltk.tree import ParentedTree,Tree
    from nltk.draw.tree import TreeWidget
    from nltk.draw.util import (CanvasFrame, CanvasWidget, BoxWidget,
                                TextWidget, ParenWidget, OvalWidget)
    from nltk.parse import CoreNLPParser
    from CodeBase.GraphParent import GraphParent

    import nltk
except ImportError:
    print('Error: cannot import the NLTK!')
    print('You need to install the NLTK. Please visit http://nltk.org/install.html for details.')
    print("On Ubuntu, the installation can be done via 'sudo apt-get install python-nltk'")
    sys.exit()

parser = CoreNLPParser(url='http://localhost:9000')
class StandfordCoreNLPEvaluator(Evaluator):
    def __init__(self, scraper):
        super().__init__(scraper)
        self.sentences = []
        dataframe = self.scraper.get_fulldf()
        for data in dataframe['text']:
            # maybe remove the (description lines)
            sent = nltk.sent_tokenize(data)
            self.sentences.extend(sent)
        self.sentence_tree=[]
    def create_trees(self):
        for s in self.sentences:
            if not s.strip():
                continue
            try:
                t = list(parser.raw_parse(s))[0]
                # print(type(t), t)
                ptree = ParentedTree.convert(t)
                self.sentence_tree.append(ptree)
            except Exception:
                # print("skipping", s)
                continue
        return self.sentence_tree