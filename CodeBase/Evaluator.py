from abc import ABC, abstractmethod
import regex as re

class Evaluator(ABC):
    """
    A base evaluator class that is intended to be inherited by other evaluators that perform specific analysis
    on scraped data. The class provides basic functionality for interacting with a Scraper object and manipulating
    file extensions.
    """
    def __init__(self, scraper=None):
        self.scraper = scraper

    @abstractmethod
    def run_evaluator(self):
        pass
    def get_json_data(self):
        """
        Returns the evaluation data in a JSON-compatible format for the file Screenplay_Raw_data.json.

        :return: Evaluation data in JSON format (default implementation returns None).
        """
        return {}
    def replace_file_extension(self,new_extension):
        """
        Adds the evaluator name to the screenplay when creating a new visualization.

        :param new_extension: The new file extension to be applied.
        :return: The filename with the new file extension.
        """
        return re.sub("\.\w+$",f"{new_extension}",self.scraper.get_filename())

