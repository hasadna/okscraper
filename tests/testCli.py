# encoding: utf-8

import unittest
from okscraper.cli.runner import Runner

class TestCli(unittest.TestCase):

    def test_runner_MainScraper(self):
        runner = Runner(module_name='mock_module')
        self.assertEqual(runner.run(), 'ok_MainScraper')

    def test_runner_OtherScraper(self):
        runner = Runner(module_name='mock_module', scraper_class_name='OtherScraper')
        self.assertEqual(runner.run(), 'ok_OtherScraper')

    def test_runner_args(self):
        runner = Runner('mock_module', None, '1', extra_data_2='2')
        self.assertEqual(runner.run(), 'ok_MainScraper12')
        runner = Runner('mock_module', 'OtherScraper', '1')
        self.assertEqual(runner.run(), 'ok_OtherScraper1')
