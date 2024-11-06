from CodeBase.Scraper import Scraper
from abc import ABC, abstractmethod


class Evaluator():
    def __init__(self, scraper=None):
        if isinstance(scraper, Scraper):
            self.scraper = scraper
        else:
            print("Initalize the scraper first before using the evaluators")
    # def get_scraper(self):
    #     return self.scraper

    # @abstractmethod
    def run_evaluator(self):
        pass

