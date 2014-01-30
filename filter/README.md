filters
-------

This subdirectory is the collection of ScraperWiki GDS filters.

Interface (see `cgi-bin/upload` which calls these filters)
----------------------------------------------------------

`def process(file_object)`

- Takes a python file handle for a spreadsheet (or similar)
- Returns the data to give to GDS (an iterable of dicts)

`def main(filename)`

- Takes a filename of a spreadsheet (or similar)
- Saves the data to the ScraperWiki data store
- Probably invokes `process` to do so

Testing
-------

Each filter should have a test file, stored in `filter/test`.
You should be able to run the test files using `nosetests`. 
You will first need to create a virtual environment and then
pip install the filter requirements file.

```shell
cd /home/tool/filter
virtualenv venv # creates a virtualenv in the ./venv directory
. venv/bin/activate
pip install -r requirements.txt
pip install nose -I
deactivate # need to refresh the virtualenv for correct `nose` to be used 
. venv/bin/activate
nosetests
```

For convenience these commands are in the script run_tests.sh.

Running the tests thereafter is as simple as doing:

```shell
cd /home/tool/filter
. venv/bin/activate
nosetests
```
