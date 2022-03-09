import os
import numpy as np
from pymatgen.util.plotting import pretty_plot, pretty_plot_two_axis, pretty_polyfit_plot
from mpl_toolkits import mplot3d
from pyplotter.io.parser import FileReader
from pyatoms.utils.utils import lazy_property
from ase.io import string2index

import logging
logger = logging.getLogger(__name__)


class Plotter(object):
    def __init__(
            self, filename, save_folder=None,
            # x_col=0, y_col=1, z_col=None,  # using python 0-index throughout
            plot_width=10,  # default plot width
            plot_height=7   # default plot height
    ):
        self.filepath = os.path.abspath(filename)
        self.filename = self.filepath.split('/')[-1]
        self.save_folder = save_folder
        self.parser = FileReader(filename=self.filepath)
        self.basename = self.parser.basename
        self.num_cols = self.parser.num_columns
        self.num_data = self.parser.num_data
        self.labels = self.parser.read_labels()
        self.data = self.parser.read_datapoints()
        # plot defaults
        # self.x_col = x_col
        # self.y_col = y_col
        # self.z_col = z_col
        # self.grouped_bar_cols_to_plot = grouped_bar_cols_to_plot
        # self.ylabel = ylabel
        # self.zlabel = zlabel

        # default ranges from data; else return None
        # if x_col is not None:
        #     # self.data_xmin = min(self.data[x_col])
        #     self.data_xmax = max(self.data[x_col])
        # if y_col is not None:
        #     self.date_ymin = min(self.data[y_col])
        #     self.data_ymax = max(self.data[y_col])
        # if z_col is not None:
        #     self.data_zmin = min(self.data[z_col])
        #     self.data_zmax = max(self.data[z_col])
        # self.bar_width = bar_width
        self.plot_width = plot_width
        self.plot_height = plot_height

        plt = pretty_plot(width=plot_width, height=plot_height)
        self.plt = plt

    # @property
    # def x_col(self):
    #     return 0
    #
    # @property
    # def y_col(self):
    #     if y_col is not None:
    #         return y_col
    #     return 1
    #
    # @property
    # def z_col(self):
    #     if z_col is not None:
    #         return z_col
    #     return 2
    #
    # @property
    # def data_xmin(self):
    #     if self.x_col is not None:
    #         data_xmin = min(self.data[self.x_col])
    #         return data_xmin
    #
    # @property
    # def data_xmax(self):
    #     if self.x_col is not None:
    #         data_xmax = max(self.data[self.x_col])
    #         return data_xmax

    def plot_2d_line_scatter_bars(
            self,
            plot_mode,
            x_col=0, y_col=1,  # cols
            bar_width=0.4,  # default width for bar plots
            grouped_bar_cols_to_plot=None,  # specify which columns to plot
            **kwargs  # kwargs to set plot parameters in self._set_plot_2d(plt=plt, **kwargs)
    ):
        assert plot_mode is not None, f'Plot mode is required!\n' \
                                      f'Available plot modes are "scatter", "line", "bar", "grouped_bar".'

        # get 2D data for plotting
        assert x_col is not None and y_col is not None, f'X and Y columns (0-indexed) need to be specified for plotting.'
        x_data = self.data[x_col]
        y_data = self.data[y_col]
        assert len(x_data) == len(y_data), f'Lens of data for plotting: {x_data} and {y_data} are not the same!'
        logger.info(f'x_data for plotting: {x_data}\n')
        logger.info(f'y_data for plotting: {y_data}\n')

        plt = self.plt

        logger.info(f'Plotting in "{plot_mode}" mode.')

        # plot the data
        if plot_mode == 'line':
            plt.plot(x_data, y_data, ls='-', lw=1.5)
        elif plot_mode == 'scatter':
            plt.scatter(x_data, y_data, marker='o', lw=1.5)
        elif plot_mode == 'bar':
            x_data = [int(i) for i in x_data]
            index = np.arange(len(x_data))
            plt.xticks(index, x_data)
            plt.bar(index, y_data, width=bar_width, color='green')
        elif plot_mode == 'grouped_bar':
            index = np.arange(1, len(x_data)+1) * self.num_cols
            x_data_labels = [str(i) for i in x_data]
            plt.xticks(index, x_data_labels)
            x_data = np.array(x_data)
            bar_width = bar_width + self.num_cols * 0.1
            if grouped_bar_cols_to_plot is not None:
                if isinstance(grouped_bar_cols_to_plot, list):
                    plot_range_list = grouped_bar_cols_to_plot
                elif isinstance(grouped_bar_cols_to_plot, str):
                    if ':' in grouped_bar_cols_to_plot:
                        plot_range_slice = string2index(grouped_bar_cols_to_plot)
                        plot_range = range(self.num_cols)
                        plot_range_list = plot_range[plot_range_slice]
                    elif ',' in grouped_bar_cols_to_plot:
                        indices = grouped_bar_cols_to_plot.split(',')
                        plot_range_list = list([int(i) for i in indices])
                    else:
                        try:
                            plot_index = string2index(grouped_bar_cols_to_plot)
                            plot_range_list = [int(plot_index)]
                        except ValueError as err:
                            logger.error(err)
                            raise
            else:
                plot_range_list = range(1, self.num_cols)  # plot all columns from 1 to the end (0-indexed)

            basename = self.basename + '_' + str(len(plot_range_list)) + '_cols'
            for i in plot_range_list:
                offset = i - self.num_cols//2
                offset_width = offset * bar_width
                logger.info(f'{self.data[i]}')
                logger.info(f'{self.labels[i]}')
                plt.bar(index + offset_width, self.data[i], width=bar_width, label=str(self.labels[i]))

        self._set_plot_2d(plt=plt, x_col=x_col, y_col=y_col, **kwargs)
        self._show_plot(plt=plt)
        self._save_plot(plt=plt, folder=self.save_folder)
        self._close_plot(plt=plt)


    def _set_plot_2d(
            self,
            plt,  # plt object to be returned
            x_col=0, y_col=1,  # cols for plotting
            ylabel=None, # specify label for y-axis
            xmin=None, xmax=None, ymin=None, ymax=None, # specify ranges for plot
            title=None # specify title for the plot
    ):
        # set plot limits
        if xmin is not None and xmax is not None:
            plt.xlim(xmin, xmax)
        elif xmax is not None:
            plt.xlim(min(self.data[x_col]), xmax)
        elif xmin is not None:
            plt.xlim(xmin, max(self.data[x_col]))

        if ymin is not None and ymax is not None:
            plt.ylim(ymin, ymax)
        elif ymax is not None:
            plt.ylim(min(self.data[y_col]), ymax)
        elif ymin is not None:
            plt.ylim(ymin, max(self.data[y_col]))

        # set up legends
        if self.labels is not None:
            logger.info(f'labels: {self.labels}')
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
        return plt

    def _save_plot(self, plt, folder=None):
        # save results
        if folder is not None:
            folder = folder
        else:
            folder = '.'
        save_filepath = os.path.join(folder, f'{self.basename}.pdf')
        save_filepath = os.path.abspath(save_filepath)
        logger.info(f'Saving file to: {save_filepath}')
        plt.savefig(save_filepath, bbox_inches='tight')

    def _show_plot(self, plt):
        plt.show()

    def _close_plot(self, plt):
        plt.clf()

    #TODO 3D plots

    def plot_3d_line_scatter_bars(
            self,
            plot_mode,
            x_col=0, y_col=1, z_col=2,  # cols
            bar_width=0.4,  # default width for bar plots
            grouped_bar_cols_to_plot=None,  # specify which columns to plot
            **kwargs  # kwargs to set plot parameters in self._set_plot_2d(plt=plt, **kwargs)
    ):
        assert plot_mode is not None, f'Plot mode is required!\n' \
                                      f'Available plot modes are "scatter", "line", "bar".'

        # get 2D data for plotting
        assert x_col is not None and y_col is not None and z_col is not None, \
            f'X and Y and Z columns (0-indexed) need to be specified for plotting.'
        x_data = self.data[x_col]
        y_data = self.data[y_col]
        z_data = self.data[z_col]
        assert len(x_data) == len(y_data) == len(z_data), \
            f'Lens of data for plotting: {x_data} and {y_data} and {z_data} are not the same!'
        logger.info(f'x_data for plotting: {x_data}\n')
        logger.info(f'y_data for plotting: {y_data}\n')
        logger.info(f'z_data for plotting: {z_data}\n')

        plt = self.plt

        # Set up Figure and 3D Axes
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        logger.info(f'Plotting in "{plot_mode}" mode.')

        # plot the data
        if plot_mode == 'line':
            ax.plot(x_data, y_data, z_data, ls='-', lw=1.5)
        elif plot_mode == 'scatter':
            ax.scatter3D(x_data, y_data, z_data, marker='o', lw=1.5)
        elif plot_mode == 'bar':
            dx = dy = dz = bar_width
            ax.bar3d(x_data, y_data, z_data, dx, dy, dz, color='green')

        self._set_plot_3d(ax=ax, x_col=x_col, y_col=y_col, z_col=z_col, **kwargs)
        self._show_plot(plt=plt)
        self._save_plot(plt=plt, folder=self.save_folder)
        self._close_plot(plt=plt)


    def _set_plot_3d(
            self,
            ax,  # plt object to be returned
            x_col=0, y_col=1, z_col=2,  # cols for plotting
            ylabel=None, # specify label for y-axis
            zlabel=None,  # specify label for y-axis
            xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None,  # specify ranges for plot
            title=None # specify title for the plot
    ):
        # set plot limits
        if xmin is not None and xmax is not None:
            ax.axes.set_xlim3d(left=xmin, right=xmax)
        elif xmax is not None:
            ax.axes.set_xlim3d(min(self.data[x_col]), xmax)
        elif xmin is not None:
            ax.axes.set_xlim3d(xmin, max(self.data[x_col]))

        if ymin is not None and ymax is not None:
            ax.axes.set_ylim3d(bottom=ymin, top=ymax)
        elif ymax is not None:
            ax.axes.set_ylim3d(min(self.data[y_col]), ymax)
        elif ymin is not None:
            ax.axes.set_ylim3d(ymin, max(self.data[y_col]))

        if zmin is not None and zmax is not None:
            ax.axes.set_zlim3d(bottom=zmin, top=zmax)
        elif ymax is not None:
            ax.axes.set_zlim3d(min(self.data[y_col]), ymax)
        elif ymin is not None:
            ax.axes.set_zlim3d(ymin, max(self.data[y_col]))

        # set up legends
        if self.labels is not None:
            logger.info(f'labels: {self.labels}')
            ax.set_xlabel(f'{self.labels[x_col].replace("_", " ")}', fontsize=24)
        if ylabel is not None:
            if '\\' in ylabel:
                ylabel_elem = ylabel.split('\\')
                ylabel = ylabel_elem[0] + f'$\{ylabel_elem[1]}$'
                ax.set_ylabel(fr'{ylabel}', fontsize=24)
            else:
                ax.set_ylabel(f'{ylabel}', fontsize=24)
        else:
            ax.set_ylabel(f'{self.labels[y_col].replace("_", " ")}', fontsize=24)

        # ax.legend(loc='upper center', ncol=self.num_data)

        # set up title
        if title is not None:
            ax.set_title(f'{title}')
        return ax


