# File upload tool

This is a ScraperWiki tool for uploading spreadsheets of a predefined format, and automatically extracting information from them.

The tool uses *filters* to do the extraction. Filters are written in Python, and will probably use the [xypath library](https://github.com/scraperwiki/xypath) for traversing grids of cells.

## Developing a filter

Brief version:

If you're a third-party developer writing a new filter, please
submit a pull request.

Currently only Python filters are supported. They should
be self-contained Python files, stored in the `filter`
directory. Each filter should contain a `main()` function which
accepts a single argument: a filename to extract (for example:
`/home/incoming/some_file.xls`). Put tests in `filter/test`.

(for more see `filter/README.md`)

