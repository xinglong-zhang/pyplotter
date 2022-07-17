import logging
logger = logging.getLogger(__name__)

from pyplotter.plotters.plots import Plotter
from matplotlib.ticker import MultipleLocator

class JobRuntimePlotter(Plotter):
    def __init__(self, filename, **kwargs):
        super().__init__(filename=filename, **kwargs)

    def plot_cores_vs_SU_per_SCF_per_atom(self, **kwargs):
        plt = self.plt
        n_cores = self.data[9]  # number of cores
        n_atoms = [int(i) for i in self.data[5]]  # number of atoms
        n_scf_iter = [int(i) for i in self.data[8]]
        elapsed_time = self.data[-2]
        SU_per_SCF_per_atom_from_elapsed_time = [
            round((elapsed_time[i]*n_cores[i])/(n_atoms[i] * n_scf_iter[i]), 10) for i in range(len(elapsed_time))
        ]
        cpu_time = self.data[-1]
        SU_per_SCF_per_atom_from_cpu_time = [
            round((cpu_time[i])/(n_atoms[i] * n_scf_iter[i]), 10) for i in range(len(cpu_time))
        ]

        SU_per_SCF_per_atom = [
            max(SU_per_SCF_per_atom_from_elapsed_time[i], SU_per_SCF_per_atom_from_cpu_time[i])
            for i in range(len(cpu_time))
        ]

        assert len(n_cores) == len(n_atoms) == len(n_scf_iter) == len(elapsed_time) \
               == len(SU_per_SCF_per_atom_from_elapsed_time)

        f = plt.figure(figsize=(10, 4))
        # ax = f.add_subplot(111)
        # ax.minorticks_on()
        #
        # # Hide the right and top spines
        # ax.spines['right'].set_visible(False)
        # ax.spines['top'].set_visible(False)
        #
        # # Only show ticks on the left and bottom spines
        # ax.yaxis.set_ticks_position('left')
        # ax.xaxis.set_ticks_position('bottom')
        #
        # if inverse_x_axis:
        #     ax.invert_xaxis()
        # print(f'n cores: {n_cores}')
        # print(f'su: {SU_per_SCF_per_atom}')

        plt.scatter(n_cores, SU_per_SCF_per_atom, 'o')
        self._set_plot_2d(plt=plt, x_col=0, y_col=1, **kwargs)
        self._save_plot(plt=plt, folder=self.save_folder)
        self._show_plot(plt=plt)
        self._close_plot(plt=plt)



