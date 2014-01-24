import subprocess
from os import listdir
from os.path import abspath, dirname, join


SCRIPTS_DIR = join(dirname(abspath(__file__)), '..')
SAMPLE_DIR = join(dirname(abspath(__file__)), '../sample_data')


def test_all_sample_data():
    files = [f for f in listdir(SCRIPTS_DIR) if f.endswith(".py")]
    fixtures = listdir(SAMPLE_DIR)

    def get_fixture_name(script):
        for f in fixtures:
            if f.startswith(script[:-len(".py")]):
                return f
        return None

    for script_name in files:
        fixture_name = get_fixture_name(script_name)
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
