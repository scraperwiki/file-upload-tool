#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import datetime
import json
import re
import sys

from collections import OrderedDict

import xypath
import scraperwiki

_DATE_RE = re.compile('(?P<month>[A-Z][a-z]{2}) (?P<year>\d{4})')


class SkipThisRow(Exception):
    pass


def main(filename):
    with open(filename, 'rb') as f:
        rows = list(process(f))
        scraperwiki.sql.save(unique_keys=["_id"], data=rows)


def process(excel_fobj):
    table = xypath.Table.from_file_object(excel_fobj, table_name='Actuals YTD')

    date_cells = get_date_cells(table)
    transaction_cells = get_transaction_cells(table)

    for date_cell, transaction_cell, volume_cell in date_cells.junction(
            transaction_cells):
        service, channel = get_service_and_channel(transaction_cell)

        try:
            yield make_row(
                transaction_cell.value,
                date_cell.value,
                volume_cell.value,
                service,
                channel
            )
        except SkipThisRow:
            pass


def get_service_and_channel(transaction_cell):
    return (get_service(transaction_cell), get_channel(transaction_cell))


def up_to_first_value(cell):
    """
    If this cell is empty, look up one cell. Return the first non-empty cell.
    """
    if not isinstance(cell.value, basestring) or cell.value.strip() != '':
        return cell
    else:
        return up_to_first_value(cell.shift(0, -1))


def get_service(transaction_cell):
    service_cell = transaction_cell.shift(-1, 0)  # 1 column left

    service_text = up_to_first_value(service_cell).value.lower()
    if 'relicensing' in service_text:
        return 'tax-disc'

    elif 'sorn' in service_text:
        return 'sorn'

    raise RuntimeError("Failed to find service: {}".format(transaction_cell))


def get_channel(transaction_cell):
    channel_cell = transaction_cell.shift(-2, 0)  # 2 columns left

    channel_text = up_to_first_value(channel_cell).value.lower()
    if 'assisted digital' in channel_text:
        return 'assisted-digital'

    elif 'fully digital' in channel_text:
        return 'fully-digital'

    elif 'manual' in channel_text:
        return 'manual'

    raise RuntimeError("Failed to find channel: {}".format(transaction_cell))


def make_row(transaction, date_text, volume, service, channel):
    volume = convert_volume(volume)
    date_time = convert_date_text(date_text)
    args = date_time, service, transaction, channel
    _id = "{0}|{1}|{2}|{3}".format(*args).replace(" ", "-")

    return OrderedDict([
        ("_id", _id),
        ("_timestamp", date_time),
        ("service", service),
        ("volume", volume),
        ("transaction", transaction),
        ("channel", channel),
    ])


def convert_volume(volume):
    if volume == '':
        raise SkipThisRow('Volume is empty string')


def convert_date_text(text):
    """
    >>> convert_date_text('Sep 2012')
    datetime.datetime(2013, 9, 1, 0, 0)
    """
    match = _DATE_RE.match(text)
    months = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
              'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
    return datetime.datetime(
        int(match.group('year')),
        months[match.group('month').lower()],
        1,
        0,  # midnight
        0
    )


def get_date_cells(table):
    date_cells = table.filter(_DATE_RE)
    assert len(date_cells) > 0
    assert len(set(cell.y for cell in date_cells)) == 1  # all on same row?
    return date_cells


def get_transaction_cells(table):
    transaction_header = table.filter_one('Transaction')

    def not_empty(cell):
        return (cell.value.strip() != '' if isinstance(cell.value, basestring)
                else True)
    transactions = transaction_header.fill(xypath.DOWN).filter(not_empty)
    return transactions

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            main(filename)
    else:
        print("Usage: {} <filename.xls>".format(sys.argv[0]))
        sys.exit(1)
