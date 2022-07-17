#!/usr/bin/env python
import click
from pyatoms.utils.logging import create_logger
from pyplotter.plotters.job_runtime_plots import JobRuntimePlotter

@click.command()
@click.option('-f', '--filename', type=str)
@click.option('-s', '--save-folder', type=str)
@click.option('-w', '--write-filename', type=str, help='Filename of plot to be saved.')
@click.option('-m', '--plot-mode', type=str, help='Options: line, scatter, bar, grouped_bar')
@click.option('-xc', '--x-col', type=int, default=None, help='x-column to plot.')
@click.option('-yc', '--y-col', type=int, default=None, help='y-column to plot.')
@click.option('-a', '--xmin', type=float, default=None)
@click.option('-x', '--xmax', type=float, default=None)
@click.option('-b', '--ymin', type=float, default=None)
@click.option('-y', '--ymax', type=float, default=None)
@click.option('-l', '--lines', type=bool, default=False, help='Plot axes lines')
@click.option('-xl', '--xlabel', default=None, help='Label for x-axis.')
@click.option('-yl', '--ylabel', default=None, help='Label for y-axis.')
@click.option('-t', '--title', type=str, default=None)
@click.option('-lf', '--label-fontsize', type=int, default=10, help='Fontsize of the axes labels.')
@click.option('-sf', '--save-format', type=str, default='pdf', help='Format of plot to be saved.')
def entry_point(filename, save_folder, write_filename, plot_mode, x_col, y_col,
                xmin, xmax, ymin, ymax, lines, xlabel, ylabel, title, label_fontsize, save_format):
    """Example usage:\n
    `plot_scan_energies.py -f iron_complexA_quartet_opt_FeC_allyl_scan_tot_ener.txt -xl "Fe-C bond distance/\AA" -yl "Relative energy/kcal mol\^{-1}" -lf 10 -r`
    """
    create_logger()
    plotter = JobRuntimePlotter(
        filename=filename, save_folder=save_folder, write_filename=write_filename,
        label_fontsize=label_fontsize, save_format=save_format
    )
    plotter.plot_cores_vs_SU_per_SCF_per_atom(
        xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, lines=lines, xlabel=xlabel, ylabel=ylabel, title=title,
    )

if __name__ == '__main__':
    entry_point()