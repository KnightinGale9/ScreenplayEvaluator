from CodeBase.Evaluator import Evaluator


class TeriorCount(Evaluator):
    def count_terior(self):
        counts = self.scraper.get_fulldf()['terior'].value_counts()
        counts.to_csv(f'{self.scraper.get_output_dir()}/{self.replace_file_extension("-terior_count.csv")}')

