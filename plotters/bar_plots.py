#!/usr/bin/env python
from pyplotter.plotters.plots import Plotter
from pyplotter.io.parser import DataParser
from pyplotter.utils.utils import spline_data
from matplotlib import pyplot as plt


class NormBarPlotter(Plotter):
    """
    Reads energy.txt and plot normalised bars
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def all_data(self):
        all_data = []
        for i in range(self.num_files):
            parser = DataParser(filename=self.files[i])
            data = parser.read_datapoints()
            # print(f'data: {data}')  # [[...], [...], [...], [...]] # four columns of data
            all_data.append(data)
        print(all_data)
        return all_data

    @property
    def all_labels(self):
        all_labels = []
        parser = DataParser(filename=self.files[0])  # sane labels for all files
        labels = parser.read_labels()
        for label in labels:
            if "_" in label:
                label = label.replace("_", " ")
            all_labels.append(label)
        return all_labels

    def plot_all(self, new_length=1000, k=3, reversed=True, x_scale=0.05, y_scale=3):
        colors = ["k", "b", "#7922BA"]
        markers = ["o", "*", "s"]

        # fig = plt.figure()
        plt.rc("font", family="Arial")
        # axis_font = {'fontname': 'Arial', 'weight': 'bold', 'size': '22'}
        plt.rc("axes", linewidth=2)

        for i in range(self.num_files):
            # data checked all correct
            x_rc = self.all_data[i][0]
            total_e = self.all_data[i][1]
            strain_e = self.all_data[i][2]
            interaction_e = self.all_data[i][3]

            # raw data points
            plt.plot(x_rc, total_e, color=colors[0], marker=markers[i], linestyle="")
            plt.plot(x_rc, strain_e, color=colors[1], marker=markers[i], linestyle="")
            plt.plot(
                x_rc, interaction_e, color=colors[2], marker=markers[i], linestyle=""
            )

            # interpolate data
            x1, y1_tot = spline_data(x_rc, total_e, new_length=new_length, k=k)
            x1, y1_strain = spline_data(x_rc, strain_e, new_length=new_length, k=k)
            x1, y1_interaction = spline_data(
                x_rc, interaction_e, new_length=new_length, k=k
            )

            plt.plot(x1, y1_tot, color=colors[0], linestyle="-")
            plt.plot(x1, y1_strain, color=colors[1], linestyle="-")
            plt.plot(x1, y1_interaction, color=colors[2], linestyle="-")

        plt.plot(x1, y1_tot, "k-", label="total")
        plt.plot(x1, y1_strain, "b-", label="distortion")
        plt.plot(
            x1, y1_interaction, color=colors[-1], linestyle="-", label="interaction"
        )

        x_min_all = []
        x_max_all = []
        y_min_all = []
        y_max_all = []

        for i in range(self.num_files):
            x_min_all.append(min(self.all_data[i][0]))
            x_max_all.append(max(self.all_data[i][0]))
            for j in range(1, 4):  # columns 2 to 4
                y_min_all.append(min(self.all_data[i][j]))
                y_max_all.append(max(self.all_data[i][j]))

        x_min = min(x_min_all)
        x_max = max(x_max_all)
        y_min = min(y_min_all)
        y_max = max(y_max_all)

        x_range = x_max - x_min
        if reversed:
            plt.xlim(x_max + x_scale * x_range, x_min - x_scale * x_range)
        else:
            plt.xlim(x_min - x_scale * x_range, x_max + x_scale * x_range)

        y_range = y_max - y_min
        plt.ylim(y_min - y_scale * y_range, y_max + y_scale * y_range)

        plt.ylabel(
            r"$E$ / kcal mol$^{-1}$", color="black", fontsize=12, fontweight="bold"
        )
        plt.xlabel(
            r"Reaction coordinate / $\AA$",
            color="black",
            fontsize=12,
            fontweight="bold",
        )

        ax = plt.gca()

        # frame visibility
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(True)
        ax.spines["left"].set_visible(True)

        ax.yaxis.set_tick_params(length=5, direction="in")

        # legend box centre top
        ax.legend(
            loc="upper center",
            ncol=3,
            frameon=True,
            columnspacing=1.5,
            prop={"size": 12},
            handletextpad=0.3,
        )
        plt.savefig("test.pdf", format="pdf", dpi=500, bbox_inches="tight")
        plt.show()
