from pathlib import Path
import regex as re

from CodeBase.HeapsLaw import HeapsLaw
from CodeBase.SceneLength import SceneLength
from CodeBase.ScreenPyScraper import ScreenPyScrapper
from CodeBase.GraphParent import GraphParent
from CodeBase.IncreasingGraph import IncreasingGraph
from CodeBase.PrescenceGraph import PrescenceGraph
from CodeBase.PartOfSpeech import PartOfSpeech
from CodeBase.SentenceComplexity import SentenceComplexity
from CodeBase.ChatGPTScraper import ChatGPTScraper
from CodeBase.SentimentAnalysis import SentimentAnalysis
from CodeBase.DirectedGraph import DirectedGraph
from CodeBase.CordGraph import CordGraph
from CodeBase.SVO import SVO

directory_path= Path("../../ScreenPy/ParserOutput/test")

for file_path in directory_path.glob("*.json"):
    with file_path.open('r') as file:
        content = file.read()
        dir_name=re.sub('\.\w+$','',file_path.name)
        mkdir=f"../output/test/{dir_name}"
        mkdir_path = Path(f"../output/test/{dir_name}")
        mkdir_path.mkdir(parents=True,exist_ok=True)


        screenplay_main=ScreenPyScrapper(mkdir,f"{directory_path}/{file_path.name}")
        screenplay_main.screenplay_scrape()
        screenplay_main.dataframe_creation()




        increasinggraph = IncreasingGraph(screenplay_main)
        increasinggraph.combined_lines()
        increasinggraph.increasing_graph()
        #
        prescencegraph = PrescenceGraph(screenplay_main)
        prescencegraph.combined_lines()
        prescencegraph.prescence_graph()
        #
        # scenelength = SceneLength(screenplay_main)
        # scenelength.create_scene_length()
        # scenelength.graph_over_time()
        # scenelength.graph_over_length()
        #
        # sentimentanalysis = SentimentAnalysis(screenplay_main)
        # sentimentanalysis.create_sentiment_list()
        # sentimentanalysis.create_graph()
        #
        heapslaw = HeapsLaw(screenplay_main)
        heapslaw.heaps_law()
        heapslaw.plot_vocab_growth()

        sentencecomplexity = SentenceComplexity(screenplay_main)
        sentencecomplexity.sentence_complexity_calculations()
        sentencecomplexity.sentence_length_graph()
        sentencecomplexity.sentence_length_indexing()
        sentencecomplexity.yngves_and_frazier_mean()
        #
        # partofspeech = PartOfSpeech(screenplay_main)
        # partofspeech.pos_aggregate()
        # partofspeech.pos_pie_chart()
        # partofspeech.key_pos_pie_chart()
        # partofspeech.noun_pie_chart()
        # partofspeech.adj_pie_chart()
        # partofspeech.adverb_pie_chart()
        # partofspeech.verb_pie_chart()
        #
        # dGraph = DirectedGraph(screenplay_main)
        # dGraph.create_directed_graph()
        # dGraph.creategraph()
        #
        # CGraph = CordGraph(screenplay_main)
        # CGraph.create_data()
        # CGraph.create_graph()
        #
        # svvo = SVO(screenplay_main)
        # svvo.create_data()
