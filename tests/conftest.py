import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--fuzz", action="store_true", default=False, help="run fuzz tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "fuzz: mark test as a fuzz test")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--fuzz"):
        skip_standard = pytest.mark.skip(reason="fuzz mode enabled, skipping standard tests")
        for item in items:
            if "fuzz" not in item.keywords:
                item.add_marker(skip_standard)

        return
    skip_fuzz = pytest.mark.skip(reason="fuzz testing, only runs when --fuzz is called")
    for item in items:
        if "fuzz" in item.keywords:
            item.add_marker(skip_fuzz)
