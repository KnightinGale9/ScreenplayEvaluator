import sys
import json

import requests

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
# Define CoreNLP server URL
CORENLP_URL = 'http://localhost:9000'

# Check if CoreNLP server is running
try:
    response = requests.get(CORENLP_URL)
    # if response.status_code != 200:
    #     raise ConnectionError(f"CoreNLP server responded with status code {response.status_code}")
except requests.exceptions.RequestException as e:
    raise ConnectionError(f"Could not connect to CoreNLP server at {CORENLP_URL}. Make sure it is running.") from e

# Initialize parser after confirming server is running
parser = CoreNLPParser(url=CORENLP_URL)
# parser = CoreNLPParser(url='http://localhost:9000')
class StandfordCoreNLPEvaluator(Evaluator):
    """
    Using Stanford NLP, generate a parse tree for each sentence. This process improves software
    efficiency by avoiding redundant parse tree generation,thereby increasing execution speed.
    Attributes:
        sentence_tree: the parse trees for each sentence.
    """
    def __init__(self, scraper):
        super().__init__(scraper)
        self.sentences = self.scraper.get_sentences()
        self.sentence_tree=[]
    def create_trees(self):
        """
        Create the parse tree for each sentence.
        :return: sentence_tree
        """
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