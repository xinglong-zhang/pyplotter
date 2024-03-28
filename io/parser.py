from pyatoms.utils.utils import lazy_property
from pyatoms.utils.logging import create_logger
logger = create_logger()


class DataParser(object):
    """
    A general file reader to read in the data for plotting
    """
    def __init__(self, filename):
        self.filename = filename

    @lazy_property
    def file_data(self):
        """ Gets the data from file and return a list of lines of the data. Includes the header line that starts with #
        Data structure of the file to be plotted:
        `````````````````````````````````````````````````````````````````````````````````````
        # header_x header_y header_z
        x_axis_value_str_int_float y_axis_value z_axis_value
        ...
        ````````````````````````````````````````````````````````````````````````````````````
        """
        contents = []
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) != 0:
                    contents.append(line)
        return contents

    @property
    def basename(self):
        return self.filename.split('/')[-1].split('.')[0]

    @property
    def num_columns(self):
        """ Get number of columns of data in the data file."""
        for line in self.file_data:
            if '#' in line:
                continue
            else:
                line_elem = line.split()
            return len(line_elem)

    @property
    def num_data(self):
        """ Get number of data to plot in the y-axis."""
        return self.num_columns - 1

    def _get_headings(self):
        headings = []
        for line in self.file_data:
            if line.startswith('#'):
                # heading line is present
                line_element = line.split('#')[-1].strip().split()
                if len(line_element) == self.num_columns:
                    # number of headings same as number of columns: x-axis has heading too
                    for i in line_element:
                        headings.append(i)
                    return headings
                elif len(line_element) == self.num_data:
                    # number of headings same as number of data: x-axis has no heading
                    headings.append('X_label')
                    for i in line_element:
                        headings.append(i)
            else:
                # when no heading is supplied
                for i in range(self.num_columns):
                    default_heading = f'column_{i+1}'
                    headings.append(default_heading)
        return headings

    @property
    def labels(self):
        return self._get_headings()

    @property
    def datapoints(self):
        return self._read_datapoints()

    def _read_datapoints(self):
        data = [[] for i in range(self.num_columns)]  # list of lists with each list a column data
        for line in self.file_data:
            if '#' in line:
                continue
            else:
                line_elem = line.split()
            for j in range(self.num_columns):
                try:
                    data[j].append(float(line_elem[j]))
                except ValueError:
                    data[j].append(line_elem[j])
        return data

    @property
    def x_data(self):
        """Return x-data as a list."""
        return self.datapoints[0]
