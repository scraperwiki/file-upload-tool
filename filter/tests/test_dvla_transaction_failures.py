#o!/usr/bin/env python
# encoding: utf-8

import datetime
import re
import unittest

from nose.tools import assert_equal, assert_almost_equal
from os.path import join, dirname, abspath

import dvla_transaction_failures

SAMPLE_DIR = join(dirname(abspath(__file__)), '../sample_data')


class ReasonForFailureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(join(
            SAMPLE_DIR,
            'dvla_transaction_failures.xls'),
                'r') as f:
            cls.rows = list(dvla_transaction_failures.process(f))

    def test_correct_number_of_rows(self):
        assert_equal(68 * 3, len(self.rows))

    def test_correct_keys(self):
        for row in self.rows:
            assert_equal(
                set(['_id', '_timestamp', 'count',
                     'description', 'reason', 'type']),
                set(row.keys()))

    def test_first_row(self):
        row = self.rows[0]
        assert_equal('2013-11-14.relicence.0', row['_id'])
        assert_equal(datetime.datetime(2013, 11, 14, 0, 0), row['_timestamp'])
        assert_equal(0, row['reason'])
        assert_equal(5, row['count'])
        assert_equal('Abandoned', row['description'])

    def test_last_row(self):
        row = self.rows[-1]
        assert_equal('2013-11-14.sorn.67', row['_id'])
        assert_equal(datetime.datetime(2013, 11, 14, 0, 0), row['_timestamp'])
        assert_equal(67, row['reason'])
        assert_equal(0, row['count'])
        assert_equal('IVR Transfer To Agent', row['description'])

    def test_ids_all_valid(self):
        for id_ in (row['_id'] for row in self.rows):
            assert isinstance(id_, basestring)
            pattern = '\d{4}-\d{2}-\d{2}.(relicence|duplicate|sorn).\d{1,2}'
            assert re.match(pattern, id_) is not None, id_


