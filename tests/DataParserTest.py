from pyplotter.io.parser import DataParser
from pyplotter.plotters.plots import Plotter
from pyplotter.plotters.errors_plots import ErrorPlotter
import logging
from pyatoms.utils.logging import create_logger
logger = logging.getLogger(__name__)
create_logger(stream=True)


class TestDataParserTest(object):
    def test_parse_data(self, tmpdir, data_for_normalisation):
        parser = DataParser(filename=data_for_normalisation)
        assert parser.num_columns == 3
        assert parser.labels == ['molecule', 'M062X/def2-SVP', 'DLPNO-CCSD(T)/CBS']