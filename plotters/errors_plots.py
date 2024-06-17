from pyplotter.utils.utils import colors
from pyplotter.plotters.plots import Plotter


class ErrorPlotter(Plotter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def plot_scatter_with_lines_and_error_bars(
        self, log=False, data_labels_list=None, x_axis_labels=None, **kwargs
    ):
        plt = self.plt
        x_data = self.data[0]
        f = plt.figure(figsize=(10, 4))
        ax = f.add_subplot(111)
        # ax.minorticks_on()

        # Hide the right and top spines
        # ax.spines['right'].set_visible(False)
        # ax.spines['top'].set_visible(False)

        # Only show ticks on the left and bottom spines
        ax.yaxis.set_ticks_position("left")
        ax.xaxis.set_ticks_position("bottom")

        # plot in log scale
        if log:
            ax.set_yscale("log")
        plt.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))

        # if inverse_x_axis:
        #     ax.invert_xaxis()

        for i in range(int(self.num_data / 2)):
            if data_labels_list is not None:
                plt.scatter(
                    x_data,
                    self.data[2 * i + 1],
                    color=colors[i],
                    ls="-",
                    label=data_labels_list[i],
                )
            else:
                plt.scatter(x_data, self.data[2 * i + 1], color=colors[i], ls="-")
            plt.errorbar(
                x_data,
                self.data[2 * i + 1],
                yerr=self.data[2 * (i + 1)],
                color=colors[i],
            )

        # change x-axis to custom
        if x_axis_labels is not None:
            assert len(x_data) == len(x_axis_labels), (
                f"Number of ticks (= {len(x_data)}) should be the same as "
                f"number of labels (= {len(x_axis_labels)})"
            )
            plt.xticks(ticks=x_data, labels=x_axis_labels)

        self._set_plot_2d(plt=plt, **kwargs)
        self._save_plot(plt=plt, folder=self.save_folder)
        self._show_plot(plt=plt)
        self._close_plot(plt=plt)
