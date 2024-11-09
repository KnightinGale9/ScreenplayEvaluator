#https://github.com/HassanElmadany/Extract-SVO?tab=readme-ov-file
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


class SVO(Evaluator):
    def find_subject(self,t):
        for s in t.subtrees(lambda t: t.label() == 'NP'):
            for n in s.subtrees(lambda n: n.label().startswith('NN')):
                return (n[0], self.find_attrs(n))


    def find_predicate(self,t):
        v = None

        for s in t.subtrees(lambda t: t.label() == 'VP'):
            for n in s.subtrees(lambda n: n.label().startswith('VB')):
                v = n
            return (v[0], self.find_attrs(v))


    def find_object(self,t):
        for s in t.subtrees(lambda t: t.label() == 'VP'):
            for n in s.subtrees(lambda n: n.label() in ['NP', 'PP', 'ADJP']):
                if n.label() in ['NP', 'PP']:
                    for c in n.subtrees(lambda c: c.label().startswith('NN')):
                        return (c[0], self.find_attrs(c))
                else:
                    for c in n.subtrees(lambda c: c.label().startswith('JJ')):
                        return (c[0], self.find_attrs(c))


    def find_attrs(self,node):
        attrs = []
        p = node.parent()

        # Search siblings
        if node.label().startswith('JJ'):
            for s in p:
                if s.label() == 'RB':
                    attrs.append(s[0])

        elif node.label().startswith('NN'):
            for s in p:
                if s.label() in ['DT', 'PRP$', 'POS', 'JJ', 'CD', 'ADJP', 'QP', 'NP']:
                    attrs.append(' '.join(s.flatten()))

        elif node.label().startswith('VB'):
            for s in p:
                if s.label() == 'ADVP':
                    attrs.append(' '.join(s.flatten()))

        # Search uncles
        if node.label().startswith('JJ') or node.label().startswith('NN'):
            for s in p.parent():
                if s != p and s.label() == 'PP':
                    attrs.append(' '.join(s.flatten()))

        elif node.label().startswith('VB'):
            for s in p.parent():
                if s != p and s.label().startswith('VB'):
                    attrs.append(s[0])

        return attrs

    def __init__(self,scraper):
        super().__init__(scraper)
        self.sentences=[]
        dataframe = self.scraper.get_fulldf()
        for data in dataframe['text']:
            #maybe remove the (description lines)
            sent = nltk.sent_tokenize(data)
            self.sentences.extend(sent)
    def calculation(self,sentence):

        # print(find_subject(sentence))
        # print(find_predicate(sentence))
        # print(find_object(sentence))
        return [self.find_subject(sentence), self.find_predicate(sentence), self.find_object(sentence)]

    import sys
    def create_data(self):
        output=[]
        # print(len(sentences))
        for s in self.sentences:
            if not s.strip():
                continue
            try:
                t = list(parser.raw_parse(s))[0]
                # print(type(t), t)
                ptree = ParentedTree.convert(t)
                output.append([s,self.calculation(ptree)])
            except Exception:
                print("skipping", s)
                continue
        # Parse the example sentence

        with open(f'{self.scraper.get_output_dir()}/{self.replace_file_extension("-SVO.json")}', "w") as f:
            json.dump(output, f)
