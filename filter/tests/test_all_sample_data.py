
import imp
import subprocess

from nose.tools import assert_greater, assert_true
from os import listdir
from os.path import abspath, dirname, join


SCRIPTS_DIR = abspath(join(dirname(__file__), '..'))
SAMPLE_DIR = abspath(join(dirname(__file__), '../sample_data'))


def get_fixtures():
    files = [f for f in listdir(SCRIPTS_DIR) if f.endswith(".py")]
    fixtures = listdir(SAMPLE_DIR)

    def get_fixture_name(script):
        for f in fixtures:
            if f.startswith(script[:-len(".py")]):
                return f
        return None

    for script_name in files:
        fixture_name = get_fixture_name(script_name)
        yield script_name, fixture_name


def test_all_sample_data():
    for script_name, fixture_name in get_fixtures():
        yield _test_one_sample_data, script_name, fixture_name


def _test_one_sample_data(script_name, fixture_name):
    if fixture_name is None:
        raise RuntimeError("No fixture for {0}".format(script_name))

    fixture_path = join(SAMPLE_DIR, fixture_name)

    try:
        # We expect this to return a zero exit status.
        # check_call will throw an exception otherwise
        subprocess.check_call(["python", script_name, fixture_path],
                              cwd=SCRIPTS_DIR,
                              env={"SCRAPERWIKI_DATABASE_NAME": ":memory:"})
    except subprocess.CalledProcessError:
        if script_name != "dummy-failure.py":
            raise


def test_all_sample_data():
    for script_name, fixture_name in get_fixtures():
        for test in _test_process(script_name, fixture_name):
            yield test


class SmallReprList(list):

    def __repr__(self):
        return "SmallReprList[{0} rows]".format(len(self))


def _test_process(script_name, fixture_name):
    if fixture_name is None:
        raise RuntimeError("No fixture for {0}".format(script_name))

    fixture_path = join(SAMPLE_DIR, fixture_name)

    module_name, _, _ = script_name.partition(".")

    if module_name == "dummy-failure":
        # dummy-failure tests will fail intentionally.
        return

    module_info = imp.find_module(module_name, [SCRIPTS_DIR])
    module = imp.load_module(module_name, *module_info)

    with open(fixture_path) as fd:
        rows = SmallReprList(module.process(fd))

    yield _test_rows_have_id, module_name, rows
    yield _test_have_any_rows, module_name, rows


def _test_rows_have_id(module_name, rows):
    assert_true(all("_id" in row for row in rows))


def _test_have_any_rows(module_name, rows):
    assert_greater(len(rows), 0)
