from matplotlib import pyplot as plt

from CodeBase.Evaluator import Evaluator

class CharacterLegend(Evaluator):
    """
     An evaluator that generates a separate character legend file for improved readability of the characters
     in the screenplay along with their corresponding colors.
    """
    def print_character_list(self):
        """
        Generates and saves a character legend as an image by retriving the character dictionary from the scraper,
        where each character is mapped to a unique color.
        :return: None(Creates the file with the extension -character_Legend.png)
        """
        colors = self.scraper.get_characterdict()
        f = lambda m, c: plt.plot([], [], marker=m, color=c, ls="none")[0]
        handles = [f("s", self.scraper.get_characterdict()[i]) for i in self.scraper.get_characterdict()]
        labels = colors
        legend = plt.legend(handles, labels, loc=3, framealpha=1, frameon=False)
        fig = legend.figure
        fig.canvas.draw()
        bbox = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        fig.savefig(f'{self.scraper.get_output_dir()}/{self.replace_file_extension( "-character_Legend.png")}', dpi="figure", bbox_inches=bbox)

