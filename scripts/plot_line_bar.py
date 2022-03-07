#!/usr/bin/env python
import click
from pyatoms.utils.logging import create_logger
from pyplotter.plotters.barplots import Plotter

@click.command()
@click.option('-f', '--filename', type=str)
@click.option('-m', '--plot-mode', type=str, help='Options: line, bar, grouped_bar')
@click.option('-c', '--cols-to-plot', default=None, help='List of columns to plot. E.g., [1:4]')
@click.option('-a', '--xmin', type=float, default=None)
@click.option('-x', '--xmax', type=float, default=None)
@click.option('-b', '--ymin', type=float, default=None)
@click.option('-y', '--ymax', type=float, default=None)
@click.option('-t', '--title', type=str, default=None)
@click.option('-w', '--width', type=float, default=0.4)
@click.option('-l', '--ylabel', type=str, default=None)
@click.option('-p', '--plot-width', type=int, default=10, help='width of the plot')
@click.option('-h', '--plot-height', type=int, default=7, help='height of the plot')
@click.option('-xc', '--x-col-num', type=int, default=1, help='1-indexed x-column number to plot.')
@click.option('-yc', '--y-col-num', type=int, default=2, help='1-indexed y-column number to plot.')

def entry_point(filename, plot_mode, cols_to_plot, xmin, xmax, ymin, ymax, title, width, ylabel, plot_width, plot_height,
                x_col_num=1, y_col_num=2):
    create_logger()
    if cols_to_plot is not None:
        cols_to_plot = eval(cols_to_plot)
    plotter = Plotter(filename=filename)
    plotter.plot_cols(
        plot_mode=plot_mode, x_column_num=x_col_num, y_column_num=y_col_num, cols_to_plot=cols_to_plot,
        xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, title=title, width=width, ylabel=ylabel,
        plot_width=plot_width, plot_height=plot_height
    )

if __name__ == '__main__':
    entry_point()