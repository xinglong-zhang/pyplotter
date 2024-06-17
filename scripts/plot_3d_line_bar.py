#!/usr/bin/env python
import click
from pyplotter.utils.utils import create_logger
from pyplotter.plotters.plots import Plotter


@click.command()
@click.option("-f", "--filename", type=str)
@click.option("-s", "--save-folder", type=str)
@click.option("-w", "--write-filename", type=str, help="Filename of plot to be saved.")
@click.option("-m", "--plot-mode", type=str, help="Options: line, scatter, bar")
@click.option("-xc", "--x-col", type=int, default=0, help="x-column to plot.")
@click.option("-yc", "--y-col", type=int, default=1, help="y-column to plot.")
@click.option("-zc", "--z-col", type=int, default=2, help="x-column to plot.")
@click.option("-b", "--bar-width", default=0.4, help="Width of bar in bar plot.")
@click.option("-a", "--xmin", type=float, default=None)
@click.option("-x", "--xmax", type=float, default=None)
@click.option("-b", "--ymin", type=float, default=None)
@click.option("-y", "--ymax", type=float, default=None)
@click.option("-c", "--zmin", type=float, default=None)
@click.option("-z", "--zmax", type=float, default=None)
@click.option("-l", "--lines", type=bool, default=False, help="Plot axes lines.")
@click.option(
    "-o",
    "--octants",
    type=bool,
    default=True,
    help="Plot axes planes to split 3D space into octants.",
)
@click.option("-xl", "--xlabel", default=None, help="Label for x-axis.")
@click.option("-yl", "--ylabel", default=None, help="Label for y-axis.")
@click.option("-zl", "--zlabel", default=None, help="Label for z-axis.")
@click.option(
    "-sc",
    "--scale-factor",
    default=0.4,
    help="Scale factor for determining ranges on axes.",
)
@click.option("-t", "--title", type=str, default=None)
@click.option("-p", "--plot-width", type=int, default=10, help="width of the plot")
@click.option("-h", "--plot-height", type=int, default=7, help="height of the plot")
@click.option(
    "-lf", "--label-fontsize", type=int, default=16, help="Fontsize of the axes labels."
)
@click.option(
    "-sf", "--save-format", type=str, default="pdf", help="Format of plot to be saved."
)
def entry_point(
    filename,
    save_folder,
    write_filename,
    plot_mode,
    x_col,
    y_col,
    z_col,
    bar_width,
    xmin,
    xmax,
    ymin,
    ymax,
    zmin,
    zmax,
    lines,
    octants,
    xlabel,
    ylabel,
    zlabel,
    scale_factor,
    title,
    plot_width,
    plot_height,
    label_fontsize,
    save_format,
):
    create_logger()
    plotter = Plotter(
        filename=filename,
        save_folder=save_folder,
        write_filename=write_filename,
        plot_width=plot_width,
        plot_height=plot_height,
        label_fontsize=label_fontsize,
        save_format=save_format,
    )
    plotter.plot_3d_line_scatter_bars(
        plot_mode=plot_mode,
        x_col=x_col,
        y_col=y_col,
        z_col=z_col,
        bar_width=bar_width,
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        ymax=ymax,
        zmin=zmin,
        zmax=zmax,
        lines=lines,
        octants=octants,
        xlabel=xlabel,
        ylabel=ylabel,
        zlabel=zlabel,
        scale_factor=scale_factor,
        title=title,
    )


if __name__ == "__main__":
    entry_point()
