import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import PchipInterpolator

from CodeBase.Evaluator import Evaluator


class DirectedGraph(Evaluator):

    def create_directed_graph(self):

        self.scraper.get_headingdf()["heading"]
        loc_graph = {}
        i = 1
        for loc in self.scraper.get_headingdf()["heading"]:
            if loc not in loc_graph:
                loc_graph[loc] = i
                i += 1
        self.char_forced_directed = {}
        for offset, char in enumerate(self.scraper.get_characterdict()):
            self.char_forced_directed[char] = {"x_val": [], "y_val": []}
            prev_loc = 0
            prev_charac = 0
            missed = 0
            for idx, row in self.scraper.get_locationdf()[["heading", char]].iterrows():
                location, charac = row

                if charac == 1:
                    missed = 0
                    self.char_forced_directed[char]["x_val"].append(idx)
                    self.char_forced_directed[char]["y_val"].append(loc_graph[location] + 0.5 * offset)
                else:
                    missed += 1
                # if charac !=1 and prev_charac==1:
                #     self.char_forced_directed[char]["x_val"].append(idx-0.5)
                #     self.char_forced_directed[char]["y_val"].append(prev_loc)
                if missed == 20:
                    self.char_forced_directed[char]["x_val"].append(np.nan)
                    self.char_forced_directed[char]["y_val"].append(np.nan)
                prev_loc = loc_graph[location]
                prev_charac = charac
        # print(x_val)
        # print(y_val)

    def creategraph(self):

        fig, ax = plt.subplots(figsize=(10, 5))

        for character in self.scraper.get_characterdict():
            if np.nan in self.char_forced_directed[character]["x_val"]:
                plt.plot(self.char_forced_directed[character]["x_val"], self.char_forced_directed[character]["y_val"], marker='o',
                         color=self.scraper.get_characterdict()[character], label='Interpolated Points')  # Line plot with markers
            else:
                # print(char_forced_directed[character]["x_val"])
                pchip_interp = PchipInterpolator(self.char_forced_directed[character]["x_val"],
                                                 self.char_forced_directed[character]["y_val"])

                # Generate new x values for smooth curve
                x_new = np.linspace(min(self.char_forced_directed[character]["x_val"]),
                                    max(self.char_forced_directed[character]["x_val"]),
                                    500)  # 500 points between the min and max of x
                y_new = pchip_interp(x_new)

                # Plot original points and interpolated curve
                plt.plot(self.char_forced_directed[character]["x_val"], self.char_forced_directed[character]["y_val"], 'o',
                         label='Original Points')  # Original points
                plt.plot(x_new, y_new, '-', label='Cubic Interpolation')  # Interpolated curve
            plt.title(character)
        plt.savefig(f'../output/{self.scraper.get_filename().replace(".json", "-DirectedGraph.png")}')
        plt.close()
