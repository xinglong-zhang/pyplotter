#!/usr/bin/env python
import click
from pyplotter.io.parser import DataParser
from pyplotter.utils.utils import spline_data
from matplotlib import pyplot as plt


class DIASPlotter(object):
    """
    Reads dias_data.txt generated from  pyatoms.analysis.dias.GaussianDIASLogFolder
    """

    def __init__(self, *args):
        self.files = args[0]
        self.num_files = len(self.files)

    @property
    def all_data(self):
        all_data = []
        for i in range(self.num_files):
            parser = DataParser(filename=self.files[i])
            data = parser.datapoints
            # print(f'data: {data}')  # [[...], [...], [...], [...]] # four columns of data
            all_data.append(data)
        # print(all_data)
        return all_data

    @property
    def all_labels(self):
        all_labels = []
        parser = DataParser(filename=self.files[0])  # sane labels for all files
        labels = parser.labels
        for label in labels:
            if "_" in label:
                label = label.replace("_", " ")
            all_labels.append(label)
        return all_labels

    def plot_all(self, new_length=1000, k=3, reversed=True, x_scale=0.05, y_scale=3):
        colors = ["k", "b", "#7922BA"]
        markers = ["*", "o", "s"]
        marker_colors = ["blue", "green", "red"]

        fig = plt.figure(figsize=(10, 6))
        plt.rc("font", family="Arial")
        axis_font = {"fontname": "Arial", "weight": "bold", "size": "22"}
        plt.rc("axes", linewidth=2)

        legend_added = False

        for i in range(self.num_files):
            # data checked all correct
            x_rc = self.all_data[i][0]
            total_e = self.all_data[i][1]
            strain_e = self.all_data[i][2]
            interaction_e = self.all_data[i][3]

            # raw data points
            plt.plot(
                x_rc,
                total_e,
                color=colors[0],
                marker=markers[i],
                markerfacecolor=marker_colors[i],
                markeredgecolor=marker_colors[i],
                linestyle="",
            )
            plt.plot(
                x_rc,
                strain_e,
                color=colors[1],
                marker=markers[i],
                markerfacecolor=marker_colors[i],
                markeredgecolor=marker_colors[i],
                linestyle="",
            )
            plt.plot(
                x_rc,
                interaction_e,
                color=colors[2],
                marker=markers[i],
                markerfacecolor=marker_colors[i],
                markeredgecolor=marker_colors[i],
                linestyle="",
            )

            if not legend_added:
                plt.legend(loc="upper center", ncols=3)
                legend_added = True

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


@click.command()
@click.option(
    "-f",
    "--filenames",
    type=str,
    multiple=True,
    help="Filenames to plot. Accepts multiple values.",
)
@click.option(
    "-l", "--new-length", type=int, default=1000, help="Number of spline points."
)
@click.option(
    "-k",
    "--k-value",
    type=int,
    default=3,
    help="Degree of the smoothing spline. Must be 1 <= k <= 5. k = 3 is a cubic spline. Default is 3.",
)
@click.option(
    "-r",
    "--reversed/--no-reversed",
    type=bool,
    default=True,
    help="Option to reverse reaction coordinates.",
)
@click.option("-x", "--x-scale", type=float, default=0.05, help="Scale along xlim.")
@click.option("-y", "--y-scale", type=float, default=3, help="Scale along y-lim.")
def entry_point(filenames, new_length, k_value, reversed, x_scale, y_scale):
    """Example usage:
    `dias_plot_all_data.py -f udc3_mCF3_c8_ts_ircr_dias_dias_data.txt -f udc3_oCF3_c6_ts_ircf_dias_dias_data.txt -y 0.05`
    `dias_plot_all_data.py -f udc3_mCF3_c8_ts_ircr_dias_gaussian_dias_zero_ref_data.txt
    -f udc3_mCF3_c8_ts_ircr_dias_orca_dias_zero_ref_data.txt -y 0.1`
    """
    dias_plotter = DIASPlotter(filenames)
    dias_plotter.plot_all(
        new_length=new_length,
        k=k_value,
        reversed=reversed,
        x_scale=x_scale,
        y_scale=y_scale,
    )


if __name__ == "__main__":
    entry_point()
