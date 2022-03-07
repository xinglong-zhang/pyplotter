import os
from pyatoms.utils.utils import lazy_property

from pyatoms.utils.logging import create_logger
logger = create_logger()


class FileReader(object):
    """
    A general file reader to read in the data for plotting
    """
    def __init__(self, filename):
        self.filename = filename

    @lazy_property
    def file_data(self):
        """
        gets the data from file
        :return:
        """
        contents = []
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith('#'):
                    pass
                else:
                    if len(line) != 0:
                        contents.append(line)
        return contents

    def _get_headings(self):
        headings = []
        with open(self.filename, 'r') as f:
            first_line = f.readlines()[0]
            if first_line.startswith('#'):
                line_element = first_line.split('#')[-1].strip().split()
                assert len(line_element) == self.num_columns, \
                    f'Number of headings should be the same as number of data columns.\n' \
                    f'Use one string per column heading.'
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
        return self.filename[:-4]

    @property
    def num_columns(self):
        for line in self.file_data:
            if '#' in line:
                line_elem = line.split('#')[0].strip().split()
            else:
                line_elem = line.split()
            return len(line_elem)

    @property
    def num_data(self):
        return self.num_columns - 1

    def read_labels(self):
        labels = self._get_headings()
        return labels

    def read_datapoints(self):
        data = [[] for i in range(self.num_columns)]  # list of lists with each list a column data
        for line in self.file_data:
            if '#' in line:
                line_elem = line.split('#')[0].strip().split()
            else:
                line_elem = line.split()
            print(f'line elem; {line_elem}')
            for j in range(self.num_columns):
                data[j].append(float(line_elem[j]))
        return data


