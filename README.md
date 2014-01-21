# File upload tool

This is a ScraperWiki tool for uploading spreadsheets of a predefined format, and automatically extracting information from them.

The tool uses *filters* to do the extraction. Filters are written in Python, and will probably use the [xypath library](https://github.com/scraperwiki/xypath) for traversing grids of cells.

Filters should have unit tests in the `/test` directory, and can store fixtures in the `/fixture` directory. If you're a third-party developer writing a new filter, please submit a pull request.
