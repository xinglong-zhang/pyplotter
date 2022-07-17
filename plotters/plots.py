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
            self, filename,
            save_folder=None,  # folder to save plot
            write_filename=None,  # filename to save plot
            plot_width=10,  # default plot width
            plot_height=7,   # default plot height
            label_fontsize=16,  # fontsize of the axes labels
            save_format='pdf',  # format of the plot to be saved
    ):
        self.filepath = os.path.abspath(filename)
        self.filename = self.filepath.split('/')[-1]
        self.save_folder = save_folder
        self.write_filename = write_filename
        if self.save_folder is None:
            self.save_folder = '.'
        self.parser = FileReader(filename=self.filepath)
        self.basename = self.parser.basename
        self.num_cols = self.parser.num_columns
        self.num_data = self.parser.num_data
        self.labels = self.parser.read_labels()
        self.data = self.parser.read_datapoints()
        self.plot_width = plot_width
        self.plot_height = plot_height
        self.label_fontsize = label_fontsize
        self.save_format = save_format

        plt = pretty_plot(width=plot_width, height=plot_height)
        self.plt = plt

    def plot_2d_line_scatter_bars(
            self,
            plot_mode,
            x_col=0, y_col=1,  # cols
            bar_width=0.4,  # default width for bar plots
            grouped_line_cols_to_plot=None,  # specify which columns to plot for multiple lines
            grouped_bar_cols_to_plot=None,  # specify which columns to plot
            **kwargs  # kwargs to set plot parameters in self._set_plot_2d(plt=plt, **kwargs)
    ):
        assert plot_mode is not None, f'Plot mode is required!\n' \
                                      f'Available plot modes are "scatter", "line", "grouped_line", "bar", "grouped_bar".'

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
        elif plot_mode == 'grouped_line':
            if grouped_line_cols_to_plot is not None:
                if isinstance(grouped_line_cols_to_plot, list):
                    plot_range_list = grouped_line_cols_to_plot
                elif isinstance(grouped_line_cols_to_plot, str):
                    if ':' in grouped_line_cols_to_plot:
                        plot_range_slice = string2index(grouped_line_cols_to_plot)
                        plot_range = range(self.num_cols)
                        plot_range_list = plot_range[plot_range_slice]
                    elif ',' in grouped_line_cols_to_plot:
                        indices = grouped_line_cols_to_plot.split(',')
                        plot_range_list = list([int(i) for i in indices])
                    else:
                        try:
                            plot_index = string2index(grouped_line_cols_to_plot)
                            plot_range_list = [int(plot_index)]
                        except ValueError as err:
                            logger.error(err)
                            raise
            else:
                plot_range_list = range(1, self.num_cols)  # plot all columns from 1 to the end (0-indexed)

            basename = self.basename + '_' + str(len(plot_range_list)) + '_cols'
            for i in plot_range_list:
                from pyplotter.utils.utils import colors
                plt.plot(x_data, self.data[i], color=colors[i], ls='-', lw=1.5)

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
        # self._turn_on_minor_ticks(ax=plt)
        self._save_plot(plt=plt, folder=self.save_folder)
        self._show_plot(plt=plt)
        self._close_plot(plt=plt)

    # def _turn_on_minor_ticks(self, plt):
    #
    #     # plt.grid(which='minor')
    #     ax.minorticks_on()
    #     # Only show ticks on the left and bottom spines
    #     ax.yaxis.set_ticks_position('left')
    #     ax.xaxis.set_ticks_position('bottom')

        # from matplotlib.ticker import MultipleLocator
        # ax.xaxis.set_minor_locator(MultipleLocator(5))
        # plt.axes().xaxis.set_minor_locator(MultipleLocator(5))
        # plt.axes().yaxis.set_minor_locator(MultipleLocator(5))
        # return ax

    def get_data_ranges(self, x_data, y_data):
        # get data ranges
        data_xmin = min(x_data)
        data_xmax = max(x_data)
        x_ranges = data_xmax - data_xmin

        data_ymin = min(y_data)
        data_ymax = max(y_data)
        y_ranges = data_ymax - data_ymin
        return data_xmin, data_xmax, x_ranges, data_ymin, data_ymax, y_ranges

    def set_data_ranges(self, xmin=None, xmax=None, ymin=None, ymax=None,
                        data_xmin=None, data_xmax=None, data_ymin=None, data_ymax=None):
        # set plot limits
        if xmin is not None and xmax is not None:
            plt.xlim(left=xmin, right=xmax)
        elif xmax is not None:
            plt.xlim(data_xmin, xmax)
        elif xmin is not None:
            plt.xlim(xmin, data_xmax)

        if ymin is not None and ymax is not None:
            plt.ylim(bottom=ymin, top=ymax)
        elif ymax is not None:
            plt.ylim(data_ymin, ymax)
        elif ymin is not None:
            plt.ylim(ymin, data_ymax)

    def _set_plot_2d(
            self,
            plt,  # plt object to be returned
            x_col=None, y_col=None,  # cols for plotting
            lines=False,  # plot x=0 and y=0 lines
            xlabel=None,  # specify label for x-axis
            ylabel=None,  # specify label for y-axis
            legend = False,  # specify legend
            xmin=None, xmax=None, ymin=None, ymax=None, # specify ranges for plot
            title=None # specify title for the plot
    ):

        if x_col is not None and y_col is not None:
            data_xmin, data_xmax, x_ranges, data_ymin, data_ymax, y_ranges \
                = self.get_data_ranges(x_data=self.data[x_col], y_data=self.data[y_col])

            self.set_data_ranges(
                xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
                data_xmin=data_xmin, data_xmax=data_xmax, data_ymin=data_ymin, data_ymax=data_ymax)

        if lines:
            # plot lines to split the quadrants
            plt.axhline(y=0, color='r', linestyle='-')
            plt.axvline(x=0, color='r', linestyle='-')

        # set up legends
        if xlabel is not None:
            if '\\' in xlabel:
                xlabel_elem = xlabel.split('\\')
                xlabel = xlabel_elem[0] + f'$\{xlabel_elem[1]}$'
                plt.xlabel(fr'{xlabel}', fontsize=self.label_fontsize)
            else:
                plt.xlabel(f'{xlabel}', fontsize=self.label_fontsize)
        else:
            if self.labels is not None and x_col is not None:
                logger.info(fr'labels: {self.labels}')
                plt.xlabel(fr'{self.labels[x_col].replace("_", " ")}', fontsize=self.label_fontsize)

        if ylabel is not None:
            if '\\' in ylabel:
                ylabel_elem = ylabel.split('\\')
                ylabel = ylabel_elem[0] + f'${ylabel_elem[1]}$'
                plt.ylabel(fr'{ylabel}', fontsize=self.label_fontsize)
            else:
                plt.ylabel(f'{ylabel}', fontsize=self.label_fontsize)
        elif ylabel is None and y_col is not None:
            plt.ylabel(f'{self.labels[y_col].replace("_", " ")}', fontsize=self.label_fontsize)
        if legend:
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
        if self.write_filename is not None:
            write_filename = self.write_filename
        else:
            # default
            write_filename = f'{self.basename}'
        save_filepath = os.path.join(folder, f'{write_filename}.{self.save_format}')
        save_filepath = os.path.abspath(save_filepath)
        logger.info(f'Saving file to: {save_filepath}')
        plt.savefig(save_filepath, bbox_inches='tight')

    def _show_plot(self, plt):
        plt.show()

    def _close_plot(self, plt):
        plt.clf()

    def plot_3d_line_scatter_bars(
            self,
            plot_mode,
            x_col=0, y_col=1, z_col=2,  # cols
            bar_width=0.4,  # default width for bar plots
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
        self._save_plot(plt=plt, folder=self.save_folder)
        self._show_plot(plt=plt)
        self._close_plot(plt=plt)

    def _set_plot_3d(
            self,
            ax,  # plt object to be returned
            x_col=0, y_col=1, z_col=2,  # cols for plotting
            lines=False,
            octant=True,
            xlabel=None,  # specify label for x-axis
            ylabel=None,  # specify label for y-axis
            zlabel=None,  # specify label for y-axis
            xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None,  # specify ranges for plot
            scale_factor=0.4,
            title=None # specify title for the plot
    ):

        # get data ranges
        data_xmin = min(self.data[x_col])
        data_xmax = max(self.data[x_col])
        x_ranges = data_xmax - data_xmin

        data_ymin = min(self.data[y_col])
        data_ymax = max(self.data[y_col])
        y_ranges = data_ymax - data_ymin

        data_zmin = min(self.data[z_col])
        data_zmax = max(self.data[z_col])
        z_ranges = data_zmax - data_zmin

        # set plots
        fig = self.plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # set plot limits
        if xmin is not None and xmax is not None:
            ax.axes.set_xlim3d(left=xmin, right=xmax)
        elif xmax is not None:
            ax.axes.set_xlim3d(data_xmin, xmax)
        elif xmin is not None:
            ax.axes.set_xlim3d(xmin, data_xmax)

        if ymin is not None and ymax is not None:
            ax.axes.set_ylim3d(bottom=ymin, top=ymax)
        elif ymax is not None:
            ax.axes.set_ylim3d(data_ymin, ymax)
        elif ymin is not None:
            ax.axes.set_ylim3d(ymin, data_ymax)

        if zmin is not None and zmax is not None:
            ax.axes.set_zlim3d(bottom=zmin, top=zmax)
        elif ymax is not None:
            ax.axes.set_zlim3d(data_zmin, ymax)
        elif ymin is not None:
            ax.axes.set_zlim3d(ymin, data_zmax)

        # get data ranges
        data_xmin = min(self.data[x_col])
        data_xmax = max(self.data[x_col])
        x_ranges = data_xmax - data_xmin

        data_ymin = min(self.data[y_col])
        data_ymax = max(self.data[y_col])
        y_ranges = data_ymax - data_ymin

        data_zmin = min(self.data[z_col])
        data_zmax = max(self.data[z_col])
        z_ranges = data_zmax - data_zmin

        if lines:
            # plot lines to split the octants
            ax.plot(
                [data_xmin - scale_factor * x_ranges, scale_factor, data_xmax + 0.1 * x_ranges],
                [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], linewidth=2, color='red'
            )
            ax.plot(
                [0.0, 0.0, 0.0],
                [data_ymin - scale_factor * y_ranges, 0.0, data_ymax + scale_factor * y_ranges],
                [0.0, 0.0, 0.0], linewidth=2, color='red'
            )
            ax.plot(
                [0.0, 0.0, 0.0], [0.0, 0.0, 0.0],
                [data_zmin - scale_factor * z_ranges, 0.0, data_zmax + scale_factor * z_ranges],
                linewidth=2, color='red'
            )

        xx_range = np.arange(data_xmin - scale_factor * x_ranges, data_xmax + scale_factor * x_ranges)
        yy_range = np.arange(data_ymin - scale_factor * y_ranges, data_ymax + scale_factor * y_ranges)
        zz_range = np.arange(data_zmin - scale_factor * z_ranges, data_zmax + scale_factor * z_ranges)

        if octant:
            # plot the planes
            xx, yy = np.meshgrid(xx_range, yy_range)
            z = xx * 0
            ax.plot_surface(xx, yy, z, alpha=0.5)

            xx, zz = np.meshgrid(xx_range, zz_range)
            y = xx * 0
            ax.plot_surface(xx, y, zz, alpha=0.5)

            yy, zz = np.meshgrid(yy_range, zz_range)
            x = zz * 0
            ax.plot_surface(x, yy, zz, alpha=0.5)

        # set up labels
        if xlabel is not None:
            self.plt.xlabel(f'{xlabel}', fontsize=self.label_fontsize)
        else:
            if self.labels is not None:
                logger.info(f'labels: {self.labels}')
                self.plt.xlabel(f'{self.labels[x_col].replace("_", " ")}', fontsize=self.label_fontsize)

        if ylabel is not None:
            if '\\' in ylabel:
                ylabel_elem = ylabel.split('\\')
                ylabel = ylabel_elem[0] + f'$\{ylabel_elem[1]}$'
                ax.set_ylabel(fr'{ylabel}', fontsize=self.label_fontsize)
            else:
                ax.set_ylabel(f'{ylabel}', fontsize=self.label_fontsize)
        else:
            ax.set_ylabel(f'{self.labels[y_col].replace("_", " ")}', fontsize=self.label_fontsize)

        if zlabel is not None:
            if '\\' in zlabel:
                zlabel_elem = zlabel.split('\\')
                zlabel = zlabel_elem[0] + f'$\{zlabel_elem[1]}$'
                ax.set_zlabel(fr'{zlabel}', fontsize=self.label_fontsize)
            else:
                ax.set_zlabel(f'{zlabel}', fontsize=self.label_fontsize)
        else:
            ax.set_zlabel(f'{self.labels[z_col].replace("_", " ")}', fontsize=self.label_fontsize)


        # ax.legend(loc='upper center', ncol=self.num_data)

        # set up title
        if title is not None:
            ax.set_title(f'{title}')
        return ax


