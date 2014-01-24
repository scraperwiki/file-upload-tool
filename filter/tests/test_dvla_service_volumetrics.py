#!/usr/bin/env python
# encoding: utf-8

import datetime
import re
import unittest

from nose.tools import assert_equal, assert_almost_equal
from os.path import join, dirname, abspath

import dvla_service_volumetrics

SAMPLE_DIR = join(dirname(abspath(__file__)), '../sample_data')


class ServiceVolumetricsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(join(
            SAMPLE_DIR,
            'dvla_service_volumetrics.xls'),
                'r') as f:
            cls.rows = list(dvla_service_volumetrics.process(f))

    def test_correct_number_of_rows(self):
        assert_equal(365, len(self.rows))

    def test_correct_keys(self):
        for row in self.rows:
            assert_equal(
                set(['_id', '_timestamp', 'service',
                     'volume', 'transaction', 'channel']),
                set(row.keys()))

    def test_correct_services(self):
        assert_equal(
            set(['sorn', 'tax-disc']),
            set([row['service'] for row in self.rows])
        )

    def test_correct_channels(self):
        assert_equal(
            set(['manual', 'assisted-digital', 'fully-digital']),
            set([row['channel'] for row in self.rows])
        )

    def test_correct_transaction_names(self):
        assert_equal(
            set([
                'V-V10 Licence Application Post Office',
                'V-V11 Licence Renewal Reminder Post Office',
                'V-V11 SORN Post Office',
                'V-V10 Licence Application EVL',
                'V-V11 Fleets',
                'V-V11 Licence Renewal Reminder EVL',
                'V-V85 and V85/1 HGV Licence Application EVL',
                'V-V11 SORN EVL',
                'V-V85/1 HGV SORN Declaration EVL',
                'V-V890 SORN Declaration EVL',
                'V-V890 SORN Declaration Fleets',
                'V-V10 Licence Application Local Office',
                'V-V11 Licence Renewal Reminder Local Office',
                'V-V85 and V85/1 HGV Licence Application',
                'V-V11 SORN Local Office',
                'V-V85/1 HGV SORN Declaration',
                'V-V890 SORN Declaration',
                'V-V890 SORN Declaration Key from Image',
                'V-V890 SORN Declaration Refunds Input',
                'V-V890 SORN Declaration Vehicles Input',
                'V-V890 SORN Declaration Vehicles Triage',
                ]),
            set([row['transaction'] for row in self.rows])
        )

    def test_first_row(self):
        row = self.rows[0]
        assert_equal(datetime.datetime(2012, 4, 1, 0, 0), row['_timestamp'])
        assert_equal('tax-disc', row['service'])
        assert_equal('assisted-digital', row['channel'])
        assert_equal(
            'V-V10 Licence Application Post Office',
            row['transaction'])

    def test_last_row(self):
        row = self.rows[-1]
        assert_equal(datetime.datetime(2013, 9, 1, 0, 0), row['_timestamp'])
        assert_equal('sorn', row['service'])
        assert_equal('manual', row['channel'])
        assert_equal(
            'V-V890 SORN Declaration Vehicles Triage',
            row['transaction'])
