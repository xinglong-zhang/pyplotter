from pyplotter.io.parser import DataParser
from pyplotter.plotters.plots import Plotter
from pyplotter.plotters.errors_plots import ErrorPlotter
import logging
from pyatoms.utils.logging import create_logger
logger = logging.getLogger(__name__)
create_logger(stream=True)


class DataParserTest(object):
    def test_parse_data(self, tmpdir, data_for_normalisation):
        parser = DataParser(filename=data_for_normalisation)
        print(parser.num_columns)