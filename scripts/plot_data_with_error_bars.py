#!/usr/bin/env python
import click
from pyplotter.utils.utils import create_logger
from pyplotter.plotters.errors_plots import ErrorPlotter


@click.command()
@click.option("-f", "--filename", type=str, help="main data file")
@click.option("-s", "--save-folder", type=str)
@click.option(
    "-ls",
    "--log-scale",
    type=bool,
    default=False,
    help="plot data in log scale, default False.",
)
@click.option("-ll", "--labels-list", default=None, help="list of legends to plot")
@click.option("-lc", "--legend-loc", default=None, help="list of legends to plot")
@click.option(
    "-xll",
    "--x-axis-labels",
    default=None,
    help="list of labels for customizing x-axis",
)
@click.option("-w", "--write-filename", type=str, help="Filename of plot to be saved.")
@click.option("-a", "--xmin", type=float, default=None)
@click.option("-x", "--xmax", type=float, default=None)
@click.option("-b", "--ymin", type=float, default=None)
@click.option("-y", "--ymax", type=float, default=None)
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
def entry_point(
    filename,
    save_folder,
    log_scale,
    labels_list,
    legend_loc,
    x_axis_labels,
    write_filename,
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
):
    """Script for plotting data with error bars. Required input will be column of data, followed by their error bars
    Example usage:\n
    `plot_data_with_error_bars.py -f all_errors_smallest_trainset.txt -ll "['MTP','Schnet','ANI']" -xll "['T2','E1','E2','E3','E4','E5','E6']" -sf svg -xl "Dataset" -yl 'Energy per atom error/eV' -lc 'best'`
    """
    create_logger()
    legend = False
    if labels_list is not None:
        labels_list = eval(labels_list)
        legend = True
    if x_axis_labels is not None:
        x_axis_labels = eval(x_axis_labels)
    plotter = ErrorPlotter(
        filename=filename,
        save_folder=save_folder,
        write_filename=write_filename,
        plot_width=plot_width,
        plot_height=plot_height,
        label_fontsize=label_fontsize,
        save_format=save_format,
    )
    plotter.plot_scatter_with_lines_and_error_bars(
        log=log_scale,
        data_labels_list=labels_list,
        legend_loc=legend_loc,
        x_axis_labels=x_axis_labels,
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
        legend=legend,
    )


if __name__ == "__main__":
    entry_point()
