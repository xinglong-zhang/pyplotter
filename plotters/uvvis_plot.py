import logging
logger = logging.getLogger(__name__)

from pyplotter.plotters.plots import Plotter

class UVVisPlotter(Plotter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def plot_wavelengths(self, first_point_ref=False, inverse_x_axis=False, **kwargs):
        plt = self.plt
        x_data = self.data[0]
        y_data = self.data[1]

        f = plt.figure(figsize=(10, 4))
        ax = f.add_subplot(111)
        ax.minorticks_on()

        # Hide the right and top spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Only show ticks on the left and bottom spines
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')

        if inverse_x_axis:
            ax.invert_xaxis()

        plt.plot(x_data, y_data, 'b-')
        self._set_plot_2d(plt=plt, x_col=0, y_col=1, **kwargs)
        self._save_plot(plt=plt, folder=self.save_folder)
        self._show_plot(plt=plt)
        self._close_plot(plt=plt)

    def read_peaks(self):
        self.parser._read_peaks()




