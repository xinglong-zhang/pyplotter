#!/usr/bin/env python
import click
import statistics
import logging
logger = logging.getLogger(__name__)
from pyplotter.utils.utils import create_logger
from pyplotter.plotters.plots import Plotter

@click.command()
@click.option('-f', '--filename', type=str)
@click.option('-c', '--column', type=int, default=0, help='column number from which to obtain data set.')
def entry_point(filename, column):
    """
    Example usage:
    `summary_stats.py -f  COLVAR -c 1`
    """
    create_logger()
    plotter = Plotter(filename=filename)

    data = plotter.data
    column_data = data[column]
    mean_value = statistics.mean(column_data)
    stdev_value = statistics.stdev(column_data)
    logger.info(f'Summary statistics: data has mean {mean_value} and standard deviation {stdev_value}')

if __name__ == '__main__':
    entry_point()