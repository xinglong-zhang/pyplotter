import os
import logging
import pytest
from pyplotter.plotters.barplots import Plotter
import logging
from pyatoms.utils.logging import create_logger
logger = logging.getLogger(__name__)
create_logger(stream=True)

class TestPlotterTest(object):
    def test_plot_two_cols(self, tmpdir, two_cols_path):
        plotter = Plotter(filename=two_cols_path, save_folder=tmpdir)
        plotter.plot_2d_line_scatter_bars(plot_mode='line')
        plotter.plot_2d_line_scatter_bars(plot_mode='scatter')
        plotter.plot_2d_line_scatter_bars(plot_mode='bar')

        plotter.plot_2d_line_scatter_bars(plot_mode='grouped_bar')  # only two cols in data
        plotter.plot_2d_line_scatter_bars(plot_mode='grouped_bar', grouped_bar_cols_to_plot='1')  # only two cols in data (x and y)

    def test_plot_five_cols(self, tmpdir, five_cols_path):
        plotter = Plotter(filename=five_cols_path, save_folder=tmpdir)
        plotter.plot_2d_line_scatter_bars(plot_mode='line')
        plotter.plot_2d_line_scatter_bars(plot_mode='scatter')
        plotter.plot_2d_line_scatter_bars(plot_mode='bar')

        plotter.plot_2d_line_scatter_bars(plot_mode='grouped_bar')  # plot all data (x and 4 y values
        plotter.plot_2d_line_scatter_bars(plot_mode='grouped_bar', grouped_bar_cols_to_plot='1')  # (x and y1)
        plotter.plot_2d_line_scatter_bars(plot_mode='grouped_bar', grouped_bar_cols_to_plot='1,2')  # (x and y1, y2)
        plotter.plot_2d_line_scatter_bars(plot_mode='grouped_bar', grouped_bar_cols_to_plot='1:4')  # (x and y1, y2, y3)
        plotter.plot_2d_line_scatter_bars(plot_mode='grouped_bar', grouped_bar_cols_to_plot=[1,2,3,4])  # (x and y1, y2, y3, y4)

        plotter.plot_2d_line_scatter_bars(plot_mode='grouped_bar', grouped_bar_cols_to_plot='2,3')  # (x and y2, y3)
        plotter.plot_2d_line_scatter_bars(plot_mode='grouped_bar', grouped_bar_cols_to_plot='1,4')  # (x and y1, y4)

