import argparse
import json
import traceback
from pathlib import Path
import regex as re
import sys
import os

import warnings
warnings.filterwarnings("ignore")
from transformers.utils.logging import set_verbosity_error
set_verbosity_error()
sys.path.append(os.path.abspath('/'))

from CodeBase.CharacterLegend import CharacterLegend
from CodeBase.HeapsLaw import HeapsLaw
from CodeBase.SentenceLengthByScene import SentenceLengthByScene
from CodeBase.TeriorCount import TeriorCount
from CodeBase.ScreenPyScraper import ScreenPyScrapper
from CodeBase.IncreasingGraph import IncreasingGraph
from CodeBase.PrescenceGraph import PrescenceGraph
from CodeBase.PartOfSpeech import PartOfSpeech
from CodeBase.SentenceComplexity import SentenceComplexity
from CodeBase.ChatGPTScraper import ChatGPTScraper
from CodeBase.SentimentAnalysis import SentimentAnalysis
from CodeBase.DirectedGraph import DirectedGraph
from CodeBase.CordGraph import CordGraph
from CodeBase.SVO import SVO
from CodeBase.StandfordCoreNLPEvaluator import  StandfordCoreNLPEvaluator

class Evaluator:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Main file to run the Screenplay Evaluators. By activating a evaluator flag only those specified will run."
                        "If no evaluator flags are called then all evaluators will run.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("input", help="Required path to directory or screenplay for files you want to run")
        parser.add_argument("output", nargs="?", default=None, help="Optional path to the output directory. Defaults to output directory")

        parser.add_argument("--charlist", help="Output the characters and corresponding colors", action='store_true', default=False)
        parser.add_argument("--increasinggraph", help="Run the increasing graph evaluator.", action='store_true', default=False)
        parser.add_argument("--prescencegraph", help="Run the presence graph evaluator.", action='store_true', default=False)
        parser.add_argument("--sentencelength", help="Run the sentence length evaluator.", action='store_true', default=False)
        parser.add_argument("--terior", help="Path to glove file or None", action='store_true', default=False)
        parser.add_argument("--heapslaw", help="Run the heaps law evaluator.", action='store_true', default=False)
        parser.add_argument("--partofspeech", help="Run the part of speech evaluator.", action='store_true', default=False)
        parser.add_argument("--directedgraph", help="Run the directed graph evaluator.", action='store_true', default=False)
        parser.add_argument("--chordgraph", help="Run the chord graph evaluator.", action='store_true', default=False)
        parser.add_argument("--sentimentanalysis", help="Run the sentiment analysis evaluator.", action='store_true', default=False)
        parser.add_argument("--sentencecomplexity", help="Run the sentence complexity graph evaluator.", action='store_true', default=False)
        parser.add_argument("--svo", help="Run the svo evaluator.", action='store_true', default=False)

        parser.add_argument("--no_log", help="Supress logging aka '-Screenplay_raw_data.json' ", action='store_false', default=True)
        parser.add_argument("--no_print", help="Supress printing", action='store_true', default=False)
        args = parser.parse_args()

        self.do_print = not args.no_print
        if not self.do_print:
            self._save_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        self.run_evaluation(args)
    def process_path(self,path):
        """Detects whether the path is a file or directory and processes it."""
        path = Path(path)  # Ensure it's a Path object
        files = []
        if path.exists():
            if path.is_file():
                print(f"Processing single file: {path.name}")
                with path.open("r", encoding="utf-8") as f:
                    content = f.read()
                files.append({"name": path.name, "content": path})
            elif path.is_dir():
                print(f"Processing directory: {path}")

                for file in path.iterdir():
                    if file.is_file():  # Ensures we only process files
                        fpath=Path(file)
                        files.append({"name": fpath.name, "content": fpath})
            return files
        else:
            print(f"Path does not exist: {path}")
            return None

    def run_evaluation(self,args):
        self.screenplay_main = None
        alleval=True
        # if you add a new evaluator flag add it to this if statement
        if  args.charlist or args.increasinggraph or args.prescencegraph or args.sentencelength or args.terior or \
            args.heapslaw or args.partofspeech or args.directedgraph  or args.chordgraph or args.svo or \
            args.sentimentanalysis or args.sentencecomplexity :
            alleval=False

        tree=None
        skipped_screenplays=[]
        print(args.input)
        files = self.process_path(args.input)
        for f in files:
            print(f["name"],f["content"])
            dir_name = re.sub(r'\.\w+$', '', f["name"])
            print(dir_name)
            if args.output is not None:
                mkdir = f"{args.output}/{dir_name}"
                mkdir_path = Path(mkdir)
                mkdir_path.mkdir(parents=True, exist_ok=True)
            else:
                print("yyyyy")
                mkdir = f"output2/{dir_name}"
                mkdir_path = Path(mkdir)
                mkdir_path.mkdir(parents=True, exist_ok=True)
            try:
                # print(f["name"])
                if ".txt" in f["name"]:
                    print("yy")
                    self.screenplay_main = ChatGPTScraper(mkdir, f["content"])
                elif ".json" in f["name"]:
                    self.screenplay_main=ScreenPyScrapper(mkdir,f["content"])
                else:
                    print("The inputted file is not the ChatGPT format or has not been parsed by screenPY")
            except Exception as e:
                print(e)
                print("The inputted file is not the correct extension, ChatGPT format, or has not been parsed by screenPY")
            if self.screenplay_main:
                try:
                    self.screenplay_main.screenplay_scrape()
                    self.screenplay_main.dataframe_creation()
                    print("Evaluators that have finished", end=": ")

                    screenplay_data = {}
                    screenplay_data["screenplay"], screenplay_data["characterdict"], screenplay_data[
                        "location_list"] = self.screenplay_main.get_json_data()

                    if args.charlist or alleval:
                        charlist = CharacterLegend(self.screenplay_main)
                        charlist.print_character_list()
                        print("Character Legend", end=", ")
                    if args.increasinggraph or alleval :
                        increasinggraph = IncreasingGraph(self.screenplay_main)
                        increasinggraph.combined_lines()
                        increasinggraph.increasing_graph()
                        screenplay_data["speaking"] = increasinggraph.get_json_data()
                        print("Increasing Graph", end=", ")
                    if args.prescencegraph or alleval:
                        prescencegraph = PrescenceGraph(self.screenplay_main)
                        prescencegraph.combined_lines()
                        prescencegraph.prescence_graph()
                        print("Presence Graph", end=", ")
                    if args.sentencelength or alleval:
                        sentlength = SentenceLengthByScene(self.screenplay_main)
                        sentlength.create_scene_length()
                        sentlength.graph_over_time()
                        sentlength.graph_over_length()
                        screenplay_data["SceneBySentence"], screenplay_data[
                            "SceneLengthBySentence"] = sentlength.get_json_data()
                        print("Sentence Length", end=", ")
                    if args.terior or alleval:
                        terior = TeriorCount(self.screenplay_main)
                        terior.count_terior()
                        print("Terior Count", end=", ")
                    if args.heapslaw or alleval:

                        heapslaw = HeapsLaw(self.screenplay_main)
                        heapslaw.heaps_law()
                        heapslaw.plot_vocab_growth()
                        screenplay_data["vocabGroth"] = heapslaw.get_json_data()
                        print("Heaps Law", end=", ")
                    if args.partofspeech or alleval:
                        partofspeech = PartOfSpeech(self.screenplay_main)
                        partofspeech.pos_aggregate()
                        partofspeech.part_of_speech_investigation()
                        partofspeech.tag_investigation()
                        screenplay_data["partofspeech"] = partofspeech.get_json_data()
                        print("Part of Speech", end=", ")
                    if  args.directedgraph or alleval:
                        dGraph = DirectedGraph(self.screenplay_main)
                        dGraph.create_directed_graph()
                        dGraph.creategraph()
                        print("Directed Graph", end=", ")
                    if args.chordgraph or alleval:
                        CGraph = CordGraph(self.screenplay_main)
                        CGraph.create_data()
                        CGraph.create_graph()
                        print("Cord Graph", end=", ")
                    if args.sentimentanalysis or alleval:
                        sentimentanalysis = SentimentAnalysis(self.screenplay_main)
                        sentimentanalysis.create_sentiment_list()
                        sentimentanalysis.create_graph()
                        screenplay_data["sentiment_percent"], screenplay_data[
                            "sentiment"] = sentimentanalysis.get_json_data()
                        print("Sentiment Analysis", end=", ")
                    if args.sentencecomplexity or args.svo:
                        coreNLPSent = StandfordCoreNLPEvaluator(self.screenplay_main)
                        tree = coreNLPSent.create_trees()
                    if args.sentencecomplexity or alleval:
                        sentencecomplexity = SentenceComplexity(self.screenplay_main, tree=tree)
                        sentencecomplexity.sentence_complexity_calculations()
                        sentencecomplexity.sentence_length_graph()
                        sentencecomplexity.sentence_length_indexing()
                        sentencecomplexity.yngves_and_frazier_mean()
                        screenplay_data["sentencecomplexity"] = sentencecomplexity.get_json_data()
                        print("Sentence Complexity", end=", ")
                    if args.svo or alleval:
                        svvo = SVO(self.screenplay_main, tree=tree)
                        svvo.create_data()
                        print("SVO")


                except Exception:
                    print(f["name"])
                    print(traceback.format_exc())
                    skipped_screenplays.append(f["name"])
                finally:
                    if args.no_log:
                        screenplay_data_file = re.sub(r"\.\w+$", f"{'-Screenplay_raw_data.json'}",
                                                        self.screenplay_main.get_filename())
                        with open(f'{self.screenplay_main.get_output_dir()}/{screenplay_data_file}', "w") as f:
                            json.dump(screenplay_data, f)

if __name__ == "__main__":
    eval_setup = Evaluator()