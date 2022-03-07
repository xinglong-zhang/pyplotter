import os
import logging
import pytest
from pyplotter.plotters.barplots import Plotter

class TestPlotterTest(object):
    def test_plot_two_cols(self, tmpdir, two_cols_path):
        plotter = Plotter(filename=two_cols_path)
        plotter.plot_cols(plot_mode='line')
        plotter.plot_cols(plot_mode='scatter')
        plotter.plot_cols(plot_mode='bar')

    def test_plot_five_cols(self, tmpdir, five_cols_path):
        plotter = Plotter(filename=five_cols_path)
        plotter.plot_cols(plot_mode='grouped_bar')
        plotter.plot_cols(plot_mode='grouped_bar', cols_to_plot=[1,2])

