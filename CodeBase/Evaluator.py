from CodeBase.Scraper import Scraper
from abc import ABC, abstractmethod
import regex as re

class Evaluator():
    def __init__(self, scraper=None):
        self.scraper = scraper
    # def get_scraper(self):
    #     return self.scraper

    # @abstractmethod
    def run_evaluator(self):
        pass
    def get_json_data(self):
        pass
    def replace_file_extension(self,new_extension):
        return re.sub("\.\w+$",f"{new_extension}",self.scraper.get_filename())

