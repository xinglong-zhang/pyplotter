import logging
import os
import pytest

logger = logging.getLogger(__name__)


@pytest.fixture()
def test_data_path():
    test_data_path = "data"
    return test_data_path


@pytest.fixture
def colvar_file(test_data_path):
    colvar_file = os.path.join(test_data_path, "COLVAR")
    return colvar_file


@pytest.fixture
def two_cols_path(test_data_path):
    two_cols_path = os.path.join(test_data_path, "two_cols_plot.txt")
    return two_cols_path


@pytest.fixture
def five_cols_path(test_data_path):
    five_cols_path = os.path.join(test_data_path, "five_cols_plot.txt")
    return five_cols_path


@pytest.fixture
def data_with_error_bars(test_data_path):
    data_with_error_bars = os.path.join(
        test_data_path, "all_errors_smallest_trainset.txt"
    )
    return data_with_error_bars


@pytest.fixture
def data_for_normalisation(test_data_path):
    data_for_normalisation = os.path.join(test_data_path, "energy_data.txt")
    return data_for_normalisation


@pytest.fixture
def uvvis_data(test_data_path):
    uvvis_data = os.path.join(test_data_path, "uvvis.txt")
    return uvvis_data
