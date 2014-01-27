#!/usr/bin/env python
# encoding: utf-8

import datetime
import re
import unittest

from nose.tools import assert_equal, assert_almost_equal
from os.path import join, dirname, abspath

import dvla_customer_satisfaction

SAMPLE_DIR = join(dirname(abspath(__file__)), '../sample_data')


class CustomerSatisfactionTest(unittest.TestCase):
    """Tests that the data inside of the actual filter is good"""
    @classmethod
    def setUpClass(cls):
        with open(join(
            SAMPLE_DIR,
            'dvla_customer_satisfaction.xls'),
                'r') as f:
            cls.rows = list(dvla_customer_satisfaction.process(f))

    def test_correct_number_of_rows(self):
        assert_equal(115, len(self.rows))

    def test_correct_keys(self):
        for row in self.rows:
            assert_equal(
                set(['_id', '_timestamp', 'satisfaction_tax_disc',
                     'satisfaction_sorn']),
                set(row.keys()))

    def test_first_row(self):
        row = self.rows[0]
        assert_equal('2004-04-01', row['_id'])
        assert_equal(datetime.datetime(2004, 4, 1, 0, 0), row['_timestamp'])
        assert_almost_equal(1.15282352941176, row['satisfaction_tax_disc'])
        assert_almost_equal(1.0, row['satisfaction_sorn'])

    def test_last_row(self):
        row = self.rows[-1]
        assert_equal('2013-10-01', row['_id'])
        assert_equal(datetime.datetime(2013, 10, 1, 0, 0), row['_timestamp'])
        assert_almost_equal(1.177107514946444, row['satisfaction_tax_disc'])
        assert_almost_equal(1.30963634059915, row['satisfaction_sorn'])

    def test_ids_all_valid(self):
        for id_ in (row['_id'] for row in self.rows):
            assert isinstance(id_, basestring)
            assert re.match('\d{4}-\d{2}-\d{2}', id_) is not None, id_
