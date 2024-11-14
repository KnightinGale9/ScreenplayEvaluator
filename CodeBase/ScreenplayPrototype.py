import json
import traceback
from pathlib import Path
import regex as re

from CodeBase.HeapsLaw import HeapsLaw
from CodeBase.SentenceLengthByScene import SentenceLengthByScene
from CodeBase.WordLengthByScene import WordLengthByScene
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

skipped_screenplays=[]

# directory_path= Path("../../ScreenPy/ParserOutput/Action")
directory_path= Path("../input")
for file_path in directory_path.glob("*.json"):
    with file_path.open('r') as file:
        content = file.read()
        print(file)
        skipfile = set(["15minutes.json","2012.json"])
        if file_path.name in skipfile:
            continue
        dir_name=re.sub('\.\w+$','',file_path.name)
        mkdir=f"../output/Action/{dir_name}"
        mkdir_path = Path(f"../output/Action/{dir_name}")
        mkdir_path.mkdir(parents=True,exist_ok=True)


        screenplay_main=ScreenPyScrapper(mkdir,f"{directory_path}/{file_path.name}")

        # screenplay_main=ChatGPTScraper(mkdir,f"{directory_path}/{file_path.name}")
        try:
            screenplay_main.screenplay_scrape()
            screenplay_main.dataframe_creation()

            screenplay_data={}
            screenplay_data["screenplay"],screenplay_data["characterdict"],screenplay_data["location_list"]=screenplay_main.get_json_data()

            increasinggraph = IncreasingGraph(screenplay_main)
            increasinggraph.combined_lines()
            increasinggraph.increasing_graph()
            screenplay_data["speaking"]=increasinggraph.get_json_data()

            prescencegraph = PrescenceGraph(screenplay_main)
            prescencegraph.combined_lines()
            prescencegraph.prescence_graph()

            sentlength = SentenceLengthByScene(screenplay_main)
            sentlength.create_scene_length()
            sentlength.graph_over_time()
            sentlength.graph_over_length()
            screenplay_data["SceneBySentence"],screenplay_data["SceneLengthBySentence"]=sentlength.get_json_data()

            wordlength = WordLengthByScene(screenplay_main)
            wordlength.create_scene_length()
            wordlength.graph_over_time()
            wordlength.graph_over_length()
            screenplay_data["SceneByWord"],screenplay_data["SceneLengthByWord"]=wordlength.get_json_data()


            sentimentanalysis = SentimentAnalysis(screenplay_main)
            sentimentanalysis.create_sentiment_list()
            sentimentanalysis.create_graph()
            screenplay_data["sentiment"]=sentimentanalysis.get_json_data()

            heapslaw = HeapsLaw(screenplay_main)
            heapslaw.heaps_law()
            heapslaw.plot_vocab_growth()
            screenplay_data["vocabGroth"]=heapslaw.get_json_data()

            sentencecomplexity = SentenceComplexity(screenplay_main)
            sentencecomplexity.sentence_complexity_calculations()
            sentencecomplexity.sentence_length_graph()
            sentencecomplexity.sentence_length_indexing()
            sentencecomplexity.yngves_and_frazier_mean()
            screenplay_data["sentencecomplexity"]=sentencecomplexity.get_json_data()

            partofspeech = PartOfSpeech(screenplay_main)
            partofspeech.pos_aggregate()
            partofspeech.part_of_speech_investigation()
            partofspeech.tag_investigation()
            screenplay_data["partofspeech"] = partofspeech.get_json_data()

            dGraph = DirectedGraph(screenplay_main)
            dGraph.create_directed_graph()
            dGraph.creategraph()

            CGraph = CordGraph(screenplay_main)
            CGraph.create_data()
            CGraph.create_graph()

            svvo = SVO(screenplay_main)
            svvo.create_data()

        except Exception:
            print(file_path.name)
            print(traceback.format_exc())
            skipped_screenplays.append(file_path.name)
        finally:
            screenplay_data_file=re.sub("\.\w+$",f"{'-Screenplay_raw_data.json'}",screenplay_main.get_filename())
            with open(f'{screenplay_main.get_output_dir()}/{screenplay_data_file}', "w") as f:
                json.dump(screenplay_data, f)
print("Screenplays that were skip due to error:",skipped_screenplays)