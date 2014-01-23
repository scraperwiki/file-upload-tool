#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import datetime
import json
import sys

from collections import OrderedDict

import xypath
from xypath import DOWN



def main(input_filename):
    raise NotImplementedError


def process(excel_fobj):
    table = xypath.Table.from_file_object(
        excel_fobj, table_name='Transaction Failures')

    def get_below(header_text):
        return table.filter(header_text).assert_one().fill(
            DOWN, stop_before=lambda cell: cell.y == last_row)

    last_row = table.filter('Total Errors').assert_one().y

    description_cells = get_below('Description')
    reason_cells = get_below('Reason for Failure')
    relicence_cells = get_below('Re-licence')
    duplicate_cells = get_below('Duplicate')
    sorn_cells = get_below('Sorn')

    date_time = table.filter('Date').shift(1, 0).value
    assert isinstance(date_time, datetime.datetime), date_time

    for description, reason, relicence, duplicate, sorn in zip(
            description_cells,
            reason_cells,
            relicence_cells,
            duplicate_cells,
            sorn_cells):
        yield make_row(date_time, description.value, reason.value, 'relicence',
                       relicence.value)
        yield make_row(date_time, description.value, reason.value, 'duplicate',
                       duplicate.value)
        yield make_row(date_time, description.value, reason.value, 'sorn',
                       sorn.value)


def make_row(date_time, description, reason_code, type_, count):
    count = int(count) if count != '' else 0
    reason_code = int(reason_code)

    assert type_ in ('relicence', 'duplicate', 'sorn'), type_
    assert description.strip() != ''

    return OrderedDict([
        ('_id', '{date}.{type_}.{reason}'.format(
            date=date_time.date().isoformat(),
            type_=type_,
            reason=reason_code)),
        ('_timestamp', date_time),
        ('reason', reason_code),
        ('description', description),
        ('type', type_),
        ('count', count),
    ])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            main(filename)
    else:
        print("Usage: {} <customer satisfaction.xls>".format(sys.argv[0]))
        sys.exit(1)
