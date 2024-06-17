from pyplotter.io.parser import DataParser
import logging
from pyplotter.utils.utils import create_logger

logger = logging.getLogger(__name__)
create_logger(stream=True)


class TestDataParserTest(object):
    def test_parse_data(self, tmpdir, data_for_normalisation):
        parser = DataParser(filename=data_for_normalisation)
        assert parser.num_columns == 3
        assert parser.labels == ["molecule", "M062X/def2-SVP", "DLPNO-CCSD(T)/CBS"]
        assert parser.datapoints == [
            [
                "UDC3-oF",
                "UDC3-mCF3",
                "UDC3-mF",
                "UDC3-o2F",
                "UDC3",
                "UDC3-mOMe",
                "UDC3-mCH3",
                "UDC3-oCF3",
                "UDC3-oOMe",
                "UDC3-o2NH2",
                "UDC3-oCH3",
                "UDC3-mNH2",
                "UDC3-oNH2",
            ],
            [
                46.3,
                46.5,
                47.7,
                45.1,
                49.4,
                55.7,
                52.3,
                50.0,
                51.8,
                55.6,
                49.0,
                57.2,
                59.3,
            ],
            [
                43.0,
                44.2,
                46.7,
                48.3,
                48.4,
                51.4,
                51.7,
                51.8,
                52.2,
                54.8,
                54.9,
                56.5,
                57.8,
            ],
        ]
        assert parser.x_data == [
            "UDC3-oF",
            "UDC3-mCF3",
            "UDC3-mF",
            "UDC3-o2F",
            "UDC3",
            "UDC3-mOMe",
            "UDC3-mCH3",
            "UDC3-oCF3",
            "UDC3-oOMe",
            "UDC3-o2NH2",
            "UDC3-oCH3",
            "UDC3-mNH2",
            "UDC3-oNH2",
        ]
