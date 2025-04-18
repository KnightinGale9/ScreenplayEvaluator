import json
import traceback
from pathlib import Path
import regex as re

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
from CodeBase.ChordGraph import CordGraph
from CodeBase.SVO import SVO
from CodeBase.StandfordCoreNLPEvaluator import  StandfordCoreNLPEvaluator

skipped_screenplays=[]

# directory_path= Path("../../ScreenPy/ParserOutput/Adventure")
# directory_path= Path("../escrow")
# directory_path= Path("../input")
# directory_path= Path("../Papernewsc")
directory_path= Path("/input")
for file_path in directory_path.glob("*.json"):
    with file_path.open('r',encoding="utf-8") as file:
        content = file.read()
        print(file)
        # 'AdventureMemorytemp1GPT4ver4.txt',
        # skipfile= set("starwarsanewhope.json")
        # skipfile = set(['127hours.json', '2001aspaceodyssey.json', 'adventuresofbuckaroobanzaiacrosstheeighthdimensionthe.json', 'armyofdarkness.json', 'beachthe.json', 'bourneidentitythe.json', 'brokenarrow.json', 'chroniclesofnarniathelionthewitchandthewardrobe.json', 'despicableme2.json', 'djangounchained.json', 'dogma.json', 'dragonslayer.json', 'e.t..json', 'escapefroml.a..json', 'escapefromnewyork.json', 'fantasticmrfox.json', 'findingnemo.json', 'fourfeathers.json', 'ghostandthedarknessthe.json', 'hellboy2thegoldenarmy.json', 'highlanderendgame.json', 'huntforredoctoberthe.json', 'imaginariumofdoctorparnassusthe.json', 'inglouriousbasterds.json', 'jurassicpark.json', 'labyrinth.json', 'legend.json', 'logansrun.json', 'lordoftheringsthetwotowers.json', 'losthorizon.json', 'madmax2theroadwarrior.json', 'missionimpossibleii.json', 'mulan.json', 'piratesofthecaribbeandeadmanschest.json', 'pokemonmewtworeturns.json', 'princessbridethe.json', 'rescuersdownunderthe.json', 'riseoftheguardians.json', 'serenity.json', 'shrek.json', 'starwarsreturnofthejedi.json', 'starwarsthephantommenace.json', 'thunderbirds.json', 'tristanandisolde.json', 'truegrit.json', 'wizardofozthe.json'])
        skipfile = set(["indianajonesandtheraidersofthelostark.json"])
        if file_path.name not in skipfile:
            continue
        dir_name=re.sub(r'\.\w+$','',file_path.name)
        mkdir=f"/output2/PaperScreenplaygenerated/{dir_name}"
        mkdir_path = Path(mkdir)
        mkdir_path.mkdir(parents=True,exist_ok=True)

        pp=Path(f"{directory_path}/{file_path.name}")
        screenplay_main=ScreenPyScrapper(mkdir,pp)
        # screenplay_main=ChatGPTScraper(mkdir,pp)
        try:
            screenplay_main.screenplay_scrape()
            screenplay_main.dataframe_creation()
            print("Evaluators that have finished", end=": ")

            screenplay_data={}
            screenplay_data["screenplay"],screenplay_data["characterdict"],screenplay_data["location_list"]=screenplay_main.get_json_data()

            charlist=CharacterLegend(screenplay_main)
            charlist.print_character_list()
            print("Character Legend", end=", ")

            increasinggraph = IncreasingGraph(screenplay_main)
            increasinggraph.combined_lines()
            increasinggraph.increasing_graph()
            screenplay_data["speaking"]=increasinggraph.get_json_data()
            print("Increasing Graph", end=", ")

            prescencegraph = PrescenceGraph(screenplay_main)
            prescencegraph.combined_lines()
            prescencegraph.prescence_graph()
            print("Presence Graph", end=", ")

            sentlength = SentenceLengthByScene(screenplay_main)
            sentlength.create_scene_length()
            sentlength.graph_over_time()
            sentlength.graph_over_length()
            screenplay_data["SceneBySentence"],screenplay_data["SceneLengthBySentence"]=sentlength.get_json_data()
            print("Sentence Length", end=", ")

            terior = TeriorCount(screenplay_main)
            terior.count_terior()
            print("Terior Count", end=", ")

            heapslaw = HeapsLaw(screenplay_main)
            heapslaw.heaps_law()
            heapslaw.plot_vocab_growth()
            screenplay_data["vocabGroth"]=heapslaw.get_json_data()
            print("Heaps Law", end=", ")

            partofspeech = PartOfSpeech(screenplay_main)
            partofspeech.pos_aggregate()
            partofspeech.part_of_speech_investigation()
            partofspeech.tag_investigation()
            screenplay_data["partofspeech"] = partofspeech.get_json_data()
            print("Part of Speech", end=", ")

            dGraph = DirectedGraph(screenplay_main)
            dGraph.create_directed_graph()
            dGraph.creategraph()
            print("Directed Graph", end=", ")

            CGraph = CordGraph(screenplay_main)
            CGraph.create_data()
            CGraph.create_graph()
            print("Cord Graph", end=", ")

            sentimentanalysis = SentimentAnalysis(screenplay_main)
            sentimentanalysis.create_sentiment_list()
            sentimentanalysis.create_graph()
            screenplay_data["sentiment_percent"],screenplay_data["sentiment"] = sentimentanalysis.get_json_data()
            print("Sentiment Analysis", end=", ")

            coreNLPSent=StandfordCoreNLPEvaluator(screenplay_main)
            tree= coreNLPSent.create_trees()

            sentencecomplexity = SentenceComplexity(screenplay_main,tree=tree)
            sentencecomplexity.sentence_complexity_calculations()
            sentencecomplexity.sentence_length_graph()
            sentencecomplexity.sentence_length_indexing()
            sentencecomplexity.yngves_and_frazier_mean()
            screenplay_data["sentencecomplexity"] = sentencecomplexity.get_json_data()
            print("Sentence Complexity", end=", ")

            svvo = SVO(screenplay_main,tree=tree)
            svvo.create_data()
            print("SVO")

        except Exception:
            print(file_path.name)
            print(traceback.format_exc())
            skipped_screenplays.append(file_path.name)
        finally:
            screenplay_data_file=re.sub(r"\.\w+$",f"{'-Screenplay_raw_data.json'}",screenplay_main.get_filename())
            with open(f'{screenplay_main.get_output_dir()}/{screenplay_data_file}', "w") as f:
                json.dump(screenplay_data, f)
print("Screenplays that were skip due to error:",skipped_screenplays)