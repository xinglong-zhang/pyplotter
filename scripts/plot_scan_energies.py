#!/usr/bin/env python
import click
from pyplotter.utils.utils import create_logger
from pyplotter.plotters.scan_energies_plots import ScanPlotter


@click.command()
@click.option("-f", "--filename", type=str)
@click.option("-s", "--save-folder", type=str)
@click.option("-w", "--write-filename", type=str, help="Filename of plot to be saved.")
@click.option(
    "-m", "--plot-mode", type=str, help="Options: line, scatter, bar, grouped_bar"
)
@click.option("-xc", "--x-col", type=int, default=0, help="x-column to plot.")
@click.option("-yc", "--y-col", type=int, default=1, help="y-column to plot.")
@click.option("-a", "--xmin", type=float, default=None)
@click.option("-x", "--xmax", type=float, default=None)
@click.option("-b", "--ymin", type=float, default=None)
@click.option("-y", "--ymax", type=float, default=None)
@click.option("-l", "--lines", type=bool, default=False, help="Plot axes lines")
@click.option("-xl", "--xlabel", default=None, help="Label for x-axis.")
@click.option("-yl", "--ylabel", default=None, help="Label for y-axis.")
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
    plot_mode,
    x_col,
    y_col,
    xmin,
    xmax,
    ymin,
    ymax,
    lines,
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
    `plot_scan_energies.py -f iron_complexA_quartet_opt_FeC_allyl_scan_tot_ener.txt -xl "Fe-C bond distance/\AA" -yl "Relative energy/kcal mol\^{-1}" -lf 10 -r`
    """
    create_logger()
    plotter = ScanPlotter(
        filename=filename,
        save_folder=save_folder,
        write_filename=write_filename,
        plot_width=plot_width,
        plot_height=plot_height,
        label_fontsize=label_fontsize,
        save_format=save_format,
    )
    plotter.plot_energy_scan(
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        lines=lines,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
        first_point_ref=reference,
        inverse_x_axis=inverse_x_axis,
    )


if __name__ == "__main__":
    entry_point()
