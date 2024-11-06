import holoviews as hv
import pandas as pd
from holoviews import opts, dim

from CodeBase.Evaluator import Evaluator

hv.extension('bokeh')
hv.output(size=200)

class CordGraph(Evaluator):
    def create_data(self):
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
        # https://holoviews.org/reference/elements/bokeh/Chord.html
        chord = hv.Chord((self.result_df))
        chord.opts(
            opts.Chord(cmap='Category20', edge_cmap='Category20', edge_color=dim('source').str(),
                       labels='name', node_color=dim('index').str()))
        hv.save(chord, f"../output/{self.scraper.get_filename().replace('.json','-chord_plot.html')}")  # for HTML
