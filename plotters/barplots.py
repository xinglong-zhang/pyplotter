import os
import numpy as np
from pymatgen.util.plotting import pretty_plot, pretty_plot_two_axis, pretty_polyfit_plot
from pyplotter.io.parser import FileReader
from pyatoms.utils.utils import lazy_property

from pyatoms.utils.logging import create_logger
logger = create_logger()


class Plotter(object):
    def __init__(self, filename):
        self.filename = filename
        self.parser = FileReader(filename=filename)
        self.basename = self.parser.basename
        self.num_cols = self.parser.num_columns
        self.num_data = self.parser.num_data
        self.labels = self.parser.read_labels()
        self.data = self.parser.read_datapoints()

    def plot_cols(
            self,
            plot_mode,
            x_column_num=1, y_column_num=2,  # 1-indexed column numbers for plotting
            cols_to_plot=None,
            ylabel=None,
            xmin=None, xmax=None, ymin=None, ymax=None, title=None,
            width=0.4,
            plot_width=10,
            plot_height=7
    ):

        assert plot_mode is not None, f'Plot mode is required!\n' \
                                      f'Available plot modes are "scatter", "line", "bar", "grouped_bar".'

        # set basename
        basename = self.basename

        # convert column to python 0-indexed numbers
        x_col = int(x_column_num) - 1
        print(f'x_col: {x_col}')
        y_col = int(y_column_num) -1
        print(f'y_col: {y_col}')
        x_data = self.data[x_col]
        y_data = self.data[y_col]
        print(f'x_data (first 15 points): {x_data[0:15]}')
        print(f'y_data (first 15 points): {y_data[0:15]}')
        assert len(x_data) == len(y_data), f'Lens of data for plotting: {x_data} and {y_data} are not the same!'

        plt = pretty_plot(width=plot_width, height=plot_height)

        print(f'Plotting in {plot_mode} mode.')

        if plot_mode == 'line':
            plt.plot(x_data, y_data, ls='-', lw=1.5)
        elif plot_mode == 'scatter':
            plt.scatter(x_data, y_data, marker='o', lw=1.5)
        elif plot_mode == 'bar':
            x_data = [int(i) for i in x_data]
            index = np.arange(len(x_data))
            plt.xticks(index, x_data)
            plt.bar(index, y_data, width=width, color='green')
        elif plot_mode == 'grouped_bar':
            index = np.arange(1, len(x_data)+1) * self.num_cols
            x_data_labels = [str(i) for i in x_data]
            plt.xticks(index, x_data_labels)
            x_data = np.array(x_data)
            bar_width = width + self.num_cols * 0.1
            if cols_to_plot is not None:
                plot_range_list = cols_to_plot
                basename = basename + '_' + str(len(plot_range_list)) + '_cols'
            else:
                plot_range_list = range(1, self.num_cols)
            for i in plot_range_list:
                offset = i - self.num_cols//2
                offset_width = offset * bar_width
                print(self.data[i])
                print(self.labels[i])
                plt.bar(index + offset_width, self.data[i], width=bar_width, label=str(self.labels[i]))

        # set plot limits
        if xmin is not None and xmax is not None:
            plt.xlim(xmin, xmax)
        if ymin is not None and ymax is not None:
            plt.ylim(ymin, ymax)

        # set up legends
        if self.labels is not None:
            print(f'labels: {self.labels}')
            plt.xlabel(f'{self.labels[x_col].replace("_", " ")}', fontsize=24)
            if ylabel is not None:
                if '\\' in ylabel:
                    ylabel_elem = ylabel.split('\\')
                    ylabel = ylabel_elem[0] + f'$\{ylabel_elem[1]}$'
                    plt.ylabel(fr'{ylabel}', fontsize=24)
                else:
                    plt.ylabel(f'{ylabel}', fontsize=24)
            else:
                plt.ylabel(f'{self.labels[y_col].replace("_", " ")}', fontsize=24)
            plt.legend(loc='upper center', ncol=self.num_data)

        # set up title
        if title is not None:
            plt.title(f'{title}')

        # save results
        plt.savefig(f'{basename}.pdf', bbox_inches='tight')
        plt.show()
        plt.clf()
