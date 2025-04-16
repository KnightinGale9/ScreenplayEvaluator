import argparse
import json
import traceback
from pathlib import Path
import regex as re
import sys
import os
#supressing torch print
import warnings

from CodeBase.CharacterGender import CharacterGender

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
from CodeBase.ChordGraph import ChordGraph
from CodeBase.SVO import SVO
from CodeBase.StandfordCoreNLPEvaluator import  StandfordCoreNLPEvaluator
from CodeBase.Pipeline import Pipeline
from CodeBase.POSCoreNLP import POSCoreNLP
class Evaluator:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Main file to run the Screenplay Evaluators. By activating a evaluator flag only those specified will run."
                        "If no evaluator flags are called then all evaluators will run.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("input", help="Required path to directory or screenplay for files you want to run")
        parser.add_argument("output", nargs="?", default=None, help="Optional path to the output directory. Defaults to output directory")

        parser.add_argument("-cl","--charlist", help="Output the characters and corresponding colors", action='store_true', default=False)
        parser.add_argument("-ig","--increasinggraph", help="Run the increasing graph evaluator.", action='store_true', default=False)
        parser.add_argument("-pg","--prescencegraph", help="Run the presence graph evaluator.", action='store_true', default=False)
        parser.add_argument("-sl","--sentencelength", help="Run the sentence length evaluator.", action='store_true', default=False)
        parser.add_argument("-t","--terior", help="Path to glove file or None", action='store_true', default=False)
        parser.add_argument("-hl","--heapslaw", help="Run the heaps law evaluator.", action='store_true', default=False)
        parser.add_argument("-pos","--partofspeech", help="Run the part of speech evaluator.", action='store_true', default=False)
        parser.add_argument("-dg","--directedgraph", help="Run the directed graph evaluator.", action='store_true', default=False)
        parser.add_argument("-cg","--chordgraph", help="Run the chord graph evaluator.", action='store_true', default=False)
        parser.add_argument("-sa","--sentimentanalysis", help="Run the sentiment analysis evaluator.", action='store_true', default=False)
        parser.add_argument("-sc","--sentencecomplexity", help="Run the sentence complexity graph evaluator.", action='store_true', default=False)
        parser.add_argument("-s","--svo", help="Run the svo evaluator.", action='store_true', default=False)
        parser.add_argument("-g","--gender", help="Run the svo evaluator.", action='store_true', default=False)

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
                # print(f"Processing single file: {path.name}")
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
            args.sentimentanalysis or args.sentencecomplexity or args.gender :
            alleval=False

        tree=None
        skipped_screenplays=[]
        # print(args.input)
        files = self.process_path(args.input)
        # print(files)
        for f in files:
            # print(f["name"],f["content"])
            dir_name = re.sub(r'\.\w+$', '', f["name"])
            print("Running evaluators on",dir_name)
            if args.output is not None:
                mkdir = f"{args.output}/{dir_name}"
                mkdir_path = Path(mkdir)
                mkdir_path.mkdir(parents=True, exist_ok=True)
            else:
                mkdir = f"output2/{dir_name}"
                mkdir_path = Path(mkdir)
                mkdir_path.mkdir(parents=True, exist_ok=True)
            try:
                # print(f["name"])
                if ".txt" in f["name"]:
                    self.screenplay_main = ChatGPTScraper(mkdir, f["content"])
                elif ".json" in f["name"]:
                    self.screenplay_main=ScreenPyScrapper(mkdir,f["content"])
                else:
                    print("The inputted file is not the ChatGPT format or has not been parsed by screenPY")
            except Exception as e:
                # print(e)
                print("The inputted file is not the correct extension, ChatGPT format, or has not been parsed by screenPY")
            if self.screenplay_main:
                try:
                    self.screenplay_main.screenplay_scrape()
                    self.screenplay_main.dataframe_creation()


                    screenplay_data = {}
                    screenplay_data["screenplay"], screenplay_data["characterdict"], screenplay_data[
                        "location_list"] = self.screenplay_main.get_json_data()
                    if args.sentencecomplexity or args.svo or args.partofspeech or alleval:
                        coreNLPSent = StandfordCoreNLPEvaluator(self.screenplay_main)
                        tree = coreNLPSent.create_trees()
                    print("Evaluators that have finished", end=": ")

                    steps= [(args.charlist, CharacterLegend(self.screenplay_main)),
                    (args.increasinggraph,IncreasingGraph(self.screenplay_main)),
                    (args.prescencegraph, PrescenceGraph(self.screenplay_main)),
                    (args.sentencelength,SentenceLengthByScene(self.screenplay_main)),
                    (args.heapslaw,HeapsLaw(self.screenplay_main)),
                    (args.partofspeech,POSCoreNLP(self.screenplay_main,tree=tree)),
                    (args.directedgraph,DirectedGraph(self.screenplay_main)),
                    (args.chordgraph,ChordGraph(self.screenplay_main)),
                    (args.sentimentanalysis, SentimentAnalysis(self.screenplay_main)),
                    (args.sentencecomplexity,SentenceComplexity(self.screenplay_main, tree=tree)),
                    (args.svo,SVO(self.screenplay_main, tree=tree)),
                    (args.gender,CharacterGender(self.screenplay_main))]

                    pipeline = Pipeline(steps)
                    screenplay_data.update(pipeline.run(alleval))

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