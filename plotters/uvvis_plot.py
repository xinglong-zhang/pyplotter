from pyplotter.plotters.plots import Plotter


class UVVisPlotter(Plotter):
    def __init__(self, include_peaks=True, os_filter=None, **kwargs):
        super().__init__(**kwargs)
        self.include_peaks = include_peaks
        self.os_filter = float(os_filter)
        wavelengths, oscillator_strength, absorptivity = self.parser._read_peaks()
        self.wavelengths = wavelengths
        self.oscillator_strength = oscillator_strength
        self.absorptivity = absorptivity

    def plot_wavelengths(self, first_point_ref=False, inverse_x_axis=False, **kwargs):
        plt = self.plt
        x_data = self.data[0]
        y_data = self.data[1]

        f = plt.figure(figsize=(10, 4))
        ax = f.add_subplot(111)
        ax.minorticks_on()

        # Hide the right and top spines
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        # Only show ticks on the left and bottom spines
        ax.yaxis.set_ticks_position("left")
        ax.xaxis.set_ticks_position("bottom")

        if inverse_x_axis:
            ax.invert_xaxis()

        plt.plot(x_data, y_data, "b-")
        if self.include_peaks:
            self.plot_peaks()
        self._set_plot_2d(plt=plt, x_col=0, y_col=1, **kwargs)
        self._save_plot(plt=plt, folder=self.save_folder)
        self._show_plot(plt=plt)
        self._close_plot(plt=plt)

    def plot_peaks(self):
        """Method to plot UV-Vis peaks information together with UV-Vis spectra"""
        plt = self.plt
        wavelengths = self.wavelengths
        oscillator_strength = self.oscillator_strength
        if self.os_filter is not None:
            filtered_values = [
                (x, y)
                for x, y in zip(wavelengths, oscillator_strength)
                if y >= self.os_filter
            ]
            wavelengths, oscillator_strength = zip(*filtered_values)

        plt.plot(wavelengths, oscillator_strength, linestyle="None", color="k")
        for x, y in zip(wavelengths, oscillator_strength):
            plt.axvline(
                x=x, ymin=0, ymax=y, color="k", linestyle="-", alpha=0.5
            )  # Plot vertical lines
