import holoviews as hv
import pandas as pd
from holoviews import opts, dim

from CodeBase.Evaluator import Evaluator

hv.extension('bokeh')
hv.output(size=200)

class CordGraph(Evaluator):
    """
    An evaluator that generates a Chord diagram representing character co-occurrence in screenplay locations.

    This class extracts character co-occurrence data, structures it into a DataFrame,
    and visualizes relationships using a Chord graph.
    Attributes:
        result_df: Hold the co-occurance connections between characters for chord diagram
    """
    def create_data(self):
        """
        Processes character co-occurrence data from the screenplay and structures it for visualization.

        The Chord diagram visually represents relationships between characters based on their co-occurrence
        in different screenplay locations.
        """
        cocur_dict = {}
        for character in self.scraper.get_characterdict():
            cocur_dict[character] = self.scraper.get_locationcocurence()[self.scraper.get_locationcocurence()[character] == 1].sum()

        cocurdf = pd.DataFrame(cocur_dict)
        matrix = cocurdf.to_numpy()


        results = []

        # Iterate through the DataFrame
        for source in cocurdf.index:
            for target in cocurdf.columns:
                if source is target:
                    continue
                value = cocurdf.loc[source, target]
                if value > 0:  # Only consider non-zero values
                    results.append((source, target, value))

        # Convert to DataFrame for better visualization (optional)
        self.result_df = pd.DataFrame(results, columns=['source', 'target', 'value'])

    def create_graph(self):
        """
        Save the bokeh chord graph in an HTML file.
        :returns: None (Creates the file with the extension -chord_plot.html)
        """
        # https://holoviews.org/reference/elements/bokeh/Chord.html
        chord = hv.Chord((self.result_df))
        chord.opts(
            opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('source').str(),
                       labels='name', node_color=dim('index').str()))
        hv.save(chord, f"{self.scraper.get_output_dir()}/{self.replace_file_extension('-chord_plot.html')}")  # for HTML
