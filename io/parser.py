import os
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

    def _get_headings(self):
        headings = []
        for line in self.file_data:
            if line.startswith('#'):
                # heading line is present
                line_element = line.split('#')[-1].strip().split()
            if line.startswith('#') and len(line_element) != self.num_columns:
                pass
            elif line.startswith('#') and len(line_element) == self.num_columns:
                for i in line_element:
                    headings.append(i)
                return headings
        else:
            # when no heading is supplied
            for i in self.num_columns:
                default_heading = f'column_{i+1}'
                headings.append(default_heading)
            return headings

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
        return self.num_columns - 1

    def read_labels(self):
        try:
            labels = self._get_headings()
            return labels
        except TypeError:
            return None

    def read_datapoints(self):
        data = [[] for i in range(self.num_columns)]  # list of lists with each list a column data
        for line in self.file_data:
            if '#' in line:
                line_elem = line.split('#')[0].strip().split()
            else:
                line_elem = line.split()
            for j in range(self.num_columns):
                try:
                    data[j].append(float(line_elem[j]))
                except ValueError:
                    data[j].append(line_elem[j])
        print(f'Data to be plotted: {data}')
        return data
