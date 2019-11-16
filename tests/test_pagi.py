#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pagi
----------------------------------

Tests for `pagi` module.
"""

import unittest

import pagi


class TestPagi(unittest.TestCase):

    def setUp(self):
        pass

    def test_something(self):
        assert(pagi.__version__)

    def tearDown(self):
        pass
