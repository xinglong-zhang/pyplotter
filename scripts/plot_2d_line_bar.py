#!/usr/bin/env python
import click
import logging
logger = logging.getLogger(__name__)
from pyatoms.utils.logging import create_logger
from pyplotter.plotters.plots import Plotter

@click.command()
@click.option('-f', '--filename', type=str)
@click.option('-s', '--save-folder', type=str)
@click.option('-w', '--write-filename', type=str, help='Filename of plot to be saved.')
@click.option('-m', '--plot-mode', type=str, help='Options: line, scatter, bar, grouped_bar, grouped_line')
@click.option('-xc', '--x-col', type=int, default=0, help='x-column to plot.')
@click.option('-yc', '--y-col', type=int, default=1, help='y-column to plot.')
@click.option('-b', '--bar-width', default=0.4, help='Width of bar in bar plot.')
@click.option('-bc', '--grouped-bar-cols-to-plot', default=None, help='Columns for grouped bar plot. Accepts list, string (e.g. "1:4" or "1,2,3,4".')
@click.option('-lc', '--grouped-line-cols-to-plot', default=None, help='Columns for grouped line plot. Accepts list, string (e.g. "1:4" or "1,2,3,4".')
@click.option('-a', '--xmin', type=float, default=None)
@click.option('-x', '--xmax', type=float, default=None)
@click.option('-b', '--ymin', type=float, default=None)
@click.option('-y', '--ymax', type=float, default=None)
@click.option('-l', '--lines', type=bool, default=False, help='Plot axes lines')
@click.option('-xl', '--xlabel', default=None, help='Label for x-axis.')
@click.option('-yl', '--ylabel', default=None, help='Label for y-axis.')
@click.option('-lg/', '--legend/--no-legend', type=bool, default=False, help='Plot axes lines')
@click.option('-t', '--title', type=str, default=None)
@click.option('-p', '--plot-width', type=int, default=10, help='Width of the plot.')
@click.option('-h', '--plot-height', type=int, default=7, help='Height of the plot.')
@click.option('-lf', '--label-fontsize', type=int, default=16, help='Fontsize of the axes labels.')
@click.option('-sf', '--save-format', type=str, default='pdf', help='Format of plot to be saved.')

def entry_point(filename, save_folder, write_filename, plot_mode, x_col, y_col,
                bar_width, grouped_line_cols_to_plot, grouped_bar_cols_to_plot,
                xmin, xmax, ymin, ymax, lines, xlabel, ylabel, legend, title,
                plot_width, plot_height, label_fontsize, save_format):
    """
    Example usage:
    `plot_2d_line_bar.py -f  train_centered_bond_distances.txt -m grouped_line -lc 1: -lg -yl "bond distance\AA" -w train_centered_bond_distances_lines`
    `plot_2d_line_bar.py -f md_centered_bond_distances.txt -m line -xc 0 -yc 1 -w md_centered_bond_distances_9_22`
    """
    create_logger()
    plotter = Plotter(
        filename=filename, save_folder=save_folder, write_filename=write_filename,
        plot_width=plot_width, plot_height=plot_height, label_fontsize=label_fontsize,
        save_format=save_format
    )
    plotter.plot_2d_line_scatter_bars(
        plot_mode=plot_mode, x_col=x_col, y_col=y_col, bar_width=bar_width,
        grouped_line_cols_to_plot=grouped_line_cols_to_plot, grouped_bar_cols_to_plot=grouped_bar_cols_to_plot,
        xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, lines=lines, xlabel=xlabel, ylabel=ylabel, legend=legend, title=title
    )

if __name__ == '__main__':
    entry_point()