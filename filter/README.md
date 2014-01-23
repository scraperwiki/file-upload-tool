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
