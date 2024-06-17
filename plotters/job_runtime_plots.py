from pyplotter.plotters.plots import Plotter


class JobRuntimePlotter(Plotter):
    def __init__(self, filename, **kwargs):
        super().__init__(filename=filename, **kwargs)
        self.logfiles = self.data[0]
        self.jobtypes = self.data[1]
        self.functionals = self.data[2]
        self.bases = self.data[3]
        self.molecules = self.data[4]
        self.n_atoms = self.data[5]
        self.n_basis_functions = self.data[6]
        self.n_primitives = self.data[7]
        self.n_scf_iters = self.data[8]
        self.n_procs = self.data[9]
        self.elapsed_times = self.data[10]
        self.cpu_times = self.data[11]
        print(self.labels)

    def plot_cores_vs_SU_per_SCF_per_atom(
        self,
        marker_size=10,
        filter_heading=None,
        filter_string_for_plotting=None,
        **kwargs,
    ):
        plt = self.plt
        n_atoms = [int(i) for i in self.n_atoms]  # number of atoms
        n_scf_iter = [int(i) for i in self.n_scf_iters]
        SU_per_SCF_per_atom_from_elapsed_time = [
            round(
                (self.elapsed_times[i] * self.n_procs[i])
                / (n_atoms[i] * self.n_scf_iters[i]),
                10,
            )
            for i in range(len(self.elapsed_times))
        ]
        SU_per_SCF_per_atom_from_cpu_time = [
            round((self.cpu_times[i]) / (n_atoms[i] * self.n_scf_iters[i]), 10)
            for i in range(len(self.cpu_times))
        ]

        SU_per_SCF_per_atom = [
            max(
                SU_per_SCF_per_atom_from_elapsed_time[i],
                SU_per_SCF_per_atom_from_cpu_time[i],
            )
            for i in range(len(self.cpu_times))
        ]

        assert (
            len(self.n_procs)
            == len(self.n_atoms)
            == len(self.n_scf_iters)
            == len(self.elapsed_times)
            == len(SU_per_SCF_per_atom_from_elapsed_time)
        )

        f = plt.figure(figsize=(10, 4))
        # plot by filter for x-axis
        if filter_heading is not None:
            try:
                filter_index = self.labels.index(filter_heading)
                filter_keys = self.data[filter_index]
                unique_filter_keys = set(filter_keys)
                if filter_string_for_plotting is None:
                    raise KeyError(
                        f"string needed for plotting. Available ones are: {unique_filter_keys}"
                    )

                x_data = []
                y_data = []
                for i in range(len(self.n_procs)):
                    if filter_string_for_plotting in unique_filter_keys:
                        if filter_keys[i] == filter_string_for_plotting:
                            x_data.append(self.n_procs[i])
                            y_data.append(SU_per_SCF_per_atom[i])
                    else:
                        raise ValueError(
                            f"String to selected for filtering data, {filter_string_for_plotting}, "
                            f"is invalid.\n Available strings are {unique_filter_keys} "
                        )
            except ValueError:
                raise ValueError(
                    f"{filter_heading} is not in the list of headings: {self.labels} \n "
                    f"for file {self.filename}"
                )
        else:
            x_data = self.n_procs
            y_data = SU_per_SCF_per_atom

        plt.scatter(x=x_data, y=y_data, marker="o", s=marker_size)
        self._set_plot_2d(plt=plt, x_col=None, y_col=None, **kwargs)
        self._save_plot(plt=plt, folder=self.save_folder)
        self._show_plot(plt=plt)
        self._close_plot(plt=plt)
