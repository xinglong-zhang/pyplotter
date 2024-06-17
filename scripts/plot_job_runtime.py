#!/usr/bin/env python
import click
from pyplotter.utils.utils import create_logger
from pyplotter.plotters.job_runtime_plots import JobRuntimePlotter


@click.command()
@click.option("-f", "--filename", type=str)
@click.option("-s", "--save-folder", type=str)
@click.option("-w", "--write-filename", type=str, help="Filename of plot to be saved.")
@click.option(
    "-m", "--marker_size", default=10, type=int, help="size of marker in scatter plot"
)
@click.option(
    "-h", "--heading", default=None, type=str, help="Heading string to apply filter on."
)
@click.option(
    "-p", "--plot-filter", default=None, type=str, help="Filter string for plotting."
)
@click.option("-xc", "--x-col", type=int, default=None, help="x-column to plot.")
@click.option("-yc", "--y-col", type=int, default=None, help="y-column to plot.")
@click.option("-a", "--xmin", type=float, default=None)
@click.option("-x", "--xmax", type=float, default=None)
@click.option("-b", "--ymin", type=float, default=None)
@click.option("-y", "--ymax", type=float, default=None)
@click.option("-xl", "--xlabel", default=None, help="Label for x-axis.")
@click.option("-yl", "--ylabel", default=None, help="Label for y-axis.")
@click.option("-t", "--title", type=str, default=None)
@click.option(
    "-lf", "--label-fontsize", type=int, default=10, help="Fontsize of the axes labels."
)
@click.option(
    "-sf", "--save-format", type=str, default="pdf", help="Format of plot to be saved."
)
def entry_point(
    filename,
    save_folder,
    write_filename,
    marker_size,
    heading,
    plot_filter,
    x_col,
    y_col,
    xmin,
    xmax,
    ymin,
    ymax,
    xlabel,
    ylabel,
    title,
    label_fontsize,
    save_format,
):
    """Example usage:\n
    `plot_job_runtime.py -f maiti_nondirected_thioarylation_runtime_data.txt -xl "Number of processors"
    -yl "SU/core-hours per atom per SCF iteration" -h Basis -p def2svp
    -w maiti_nondirected_thioarylation_runtime_data_def2svp `
    """
    create_logger()
    plotter = JobRuntimePlotter(
        filename=filename,
        save_folder=save_folder,
        write_filename=write_filename,
        label_fontsize=label_fontsize,
        save_format=save_format,
    )
    plotter.plot_cores_vs_SU_per_SCF_per_atom(
        marker_size=marker_size,
        filter_heading=heading,
        filter_string_for_plotting=plot_filter,
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
    )


if __name__ == "__main__":
    entry_point()
