#!/usr/bin/env python
import click
from pyplotter.utils.utils import create_logger
from pyplotter.plotters.uvvis_plot import UVVisPlotter


@click.command()
@click.option("-f", "--filename", type=str)
@click.option("-s", "--save-folder", type=str)
@click.option("-w", "--write-filename", type=str, help="Filename of plot to be saved.")
@click.option(
    "-o",
    "--os-filter",
    type=float,
    default=0.05,
    help="Filter value for oscillator strength below which the peaks are not plotted.",
)
@click.option("-a", "--xmin", type=float, default=100)
@click.option("-x", "--xmax", type=float, default=1500)
@click.option("-b", "--ymin", type=float, default=None)
@click.option("-y", "--ymax", type=float, default=None)
@click.option("-xl", "--xlabel", default="Wavelength / nm", help="Label for x-axis.")
@click.option(
    "-yl",
    "--ylabel",
    default="Molar absorptivity / L mol$^{-1}$ cm$^{-1}$",
    help="Label for y-axis.",
)
@click.option("-t", "--title", type=str, default=None)
@click.option("-p", "--plot-width", type=int, default=10, help="Width of the plot.")
@click.option("-h", "--plot-height", type=int, default=7, help="Height of the plot.")
@click.option(
    "-lf", "--label-fontsize", type=int, default=10, help="Fontsize of the axes labels."
)
@click.option(
    "-sf", "--save-format", type=str, default="pdf", help="Format of plot to be saved."
)
@click.option(
    "-r",
    "--reference/--no-reference",
    type=bool,
    default=False,
    help="To take first data point as energy min for reference.",
)
@click.option(
    "-i",
    "--inverse-x-axis/--no-inverse-x-axis",
    type=bool,
    default=False,
    help="Inverse x-axis.",
)
def entry_point(
    filename,
    save_folder,
    write_filename,
    os_filter,
    xmin,
    xmax,
    ymin,
    ymax,
    xlabel,
    ylabel,
    title,
    plot_width,
    plot_height,
    label_fontsize,
    save_format,
    reference,
    inverse_x_axis,
):
    """Example usage:\n
    `plot_uvvis.py -f pop1_ketone_model_opt_radical_anion_r1s50_gas_uvvis.txt -a 200 -x 1000 -o 0.05
    """
    create_logger()
    plotter = UVVisPlotter(
        filename=filename,
        save_folder=save_folder,
        write_filename=write_filename,
        plot_width=plot_width,
        plot_height=plot_height,
        label_fontsize=label_fontsize,
        save_format=save_format,
        os_filter=os_filter,
    )
    plotter.plot_wavelengths(
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
        first_point_ref=reference,
        inverse_x_axis=inverse_x_axis,
    )


if __name__ == "__main__":
    entry_point()
