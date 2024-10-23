from CodeBase.Scraper import Scraper

class Evaluator():
    def __init(self, scraper=None):
        if isinstance(scraper, Scraper):
            self.scraper = scraper
        else:
            print("Initalize the scraper first before using the evaluators")
    def get_scraper(self):
        return self.scraper

