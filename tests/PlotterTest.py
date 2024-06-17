import logging
from pyplotter.plotters.plots import Plotter
from pyplotter.plotters.errors_plots import ErrorPlotter
from pyplotter.plotters.uvvis_plot import UVVisPlotter
from pyplotter.utils.utils import create_logger

logger = logging.getLogger(__name__)
create_logger()


class TestPlotterTest(object):
    def test_plot_two_cols(self, tmpdir, two_cols_path):
        plotter = Plotter(filename=two_cols_path, save_folder=tmpdir)
        plotter.plot_2d_line_scatter_bars(plot_mode="line")
        plotter.plot_2d_line_scatter_bars(plot_mode="scatter")
        plotter.plot_2d_line_scatter_bars(plot_mode="bar")

        plotter.plot_2d_line_scatter_bars(
            plot_mode="grouped_bar"
        )  # only two cols in data
        plotter.plot_2d_line_scatter_bars(
            plot_mode="grouped_bar", grouped_bar_cols_to_plot="1"
        )  # only two cols in data (x and y)

    def test_plot_five_cols(self, tmpdir, five_cols_path):
        plotter = Plotter(filename=five_cols_path, save_folder=tmpdir)
        plotter.plot_2d_line_scatter_bars(plot_mode="line")
        plotter.plot_2d_line_scatter_bars(
            plot_mode="grouped_line", grouped_line_cols_to_plot="2,3"
        )  # (x and y1, y2)
        plotter.plot_2d_line_scatter_bars(plot_mode="scatter")
        plotter.plot_2d_line_scatter_bars(plot_mode="bar")
        plotter.plot_2d_line_scatter_bars(plot_mode="bar", x_col=0, y_col=2)

        plotter.plot_2d_line_scatter_bars(
            plot_mode="grouped_bar"
        )  # plot all data (x and 4 y values
        plotter.plot_2d_line_scatter_bars(
            plot_mode="grouped_bar", grouped_bar_cols_to_plot="1"
        )  # (x and y1)
        plotter.plot_2d_line_scatter_bars(
            plot_mode="grouped_bar", grouped_bar_cols_to_plot="1,2"
        )  # (x and y1, y2)
        plotter.plot_2d_line_scatter_bars(
            plot_mode="grouped_bar", grouped_bar_cols_to_plot="1:4"
        )  # (x and y1, y2, y3)
        plotter.plot_2d_line_scatter_bars(
            plot_mode="grouped_bar", grouped_bar_cols_to_plot=[1, 2, 3, 4]
        )  # (x and y1, y2, y3, y4)

        plotter.plot_2d_line_scatter_bars(
            plot_mode="grouped_bar", grouped_bar_cols_to_plot="2,3"
        )  # (x and y2, y3)
        plotter.plot_2d_line_scatter_bars(
            plot_mode="grouped_bar", grouped_bar_cols_to_plot="1,4"
        )  # (x and y1, y4)

    def test_plot_five_cols_3d(self, tmpdir, five_cols_path):
        plotter = Plotter(filename=five_cols_path, save_folder=tmpdir)
        plotter.plot_3d_line_scatter_bars(plot_mode="line")
        plotter.plot_3d_line_scatter_bars(plot_mode="line", x_col=0, y_col=0, z_col=0)
        plotter.plot_3d_line_scatter_bars(plot_mode="scatter")
        plotter.plot_3d_line_scatter_bars(
            plot_mode="scatter", x_col=0, y_col=0, z_col=0
        )
        plotter.plot_3d_line_scatter_bars(plot_mode="bar", title="test")

    def test_plot_with_error_bars(self, tmpdir, data_with_error_bars):
        plotter = ErrorPlotter(filename=data_with_error_bars, save_folder=tmpdir)
        plotter.plot_scatter_with_lines_and_error_bars(
            data_labels_list=["MTP", "Schnet", "ANI"]
        )

    def test_plot_uvvis_data(self, tmpdir, uvvis_data):
        plotter = UVVisPlotter(filename=uvvis_data, save_folder=tmpdir, os_filter=0.1)
        plotter.plot_wavelengths(
            xlabel="wavelength / nm",
            ylabel="Molar absorptivity / L mol$^{-1}$ cm$^{-1}$",
        )
