#!/usr/bin/env python
# encoding: utf-8

"""Read spreadsheets like dvla_customer_satisfaction.xls"""

from __future__ import unicode_literals

import datetime
import sys

from collections import OrderedDict

import xypath
import scraperwiki


def main(filename):
    with open(filename, 'rb') as f:
        rows = list(process(f))
        scraperwiki.sql.save(unique_keys=["_id"], data=rows)


def process(excel_fobj):
    table = xypath.Table.from_file_object(excel_fobj, table_name='Table')

    date_cells = get_date_cells(table)
    tax_disc_header = table.filter('Relicensing').assert_one()
    sorn_header = table.filter('SORN').assert_one()

    for date_cell in date_cells:
        yield process_date_row(date_cell, tax_disc_header, sorn_header)


def process_date_row(date_cell, tax_disc_header, sorn_header):
    assert isinstance(date_cell.value, datetime.datetime)
    date = date_cell.value.date()

    (_, _, satisfaction_tax_disc_cell) = next(
        date_cell.junction(tax_disc_header))
    satisfaction_tax_disc = satisfaction_tax_disc_cell.value

    (_, _, satisfaction_sorn_cell) = next(
        date_cell.junction(sorn_header))
    satisfaction_sorn = satisfaction_sorn_cell.value

    return OrderedDict([
        ('_id', date.isoformat()),  # string
        ('_timestamp', datetime.datetime.combine(date, datetime.time())),
        ('satisfaction_tax_disc', satisfaction_tax_disc),
        ('satisfaction_sorn', satisfaction_sorn),
    ])


def get_date_cells(table):
    start_cell = table.filter('Date of Liability').assert_one()
    stop_cell = table.filter('Grand Total').assert_one()

    date_cells = start_cell.fill(
        xypath.DOWN,
        stop_before=lambda cell: cell == stop_cell)

    for cell in date_cells:
        if not isinstance(cell.value, datetime.date):
            raise RuntimeError("'{}' : {}".format(cell.value, cell.value.__class__))
    return date_cells

if __name__ == "__main__":
    main(sys.argv[1])
