# encoding: utf-8

import unittest
import logging
from okscraper.cli.runner import Runner, LogRunner, DbLogRunner

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


class DummyLogHandler(logging.Handler):

    def __init__(self, *args, **kwargs):
        super(DummyLogHandler, self).__init__(*args, **kwargs)
        self.logs = []

    def emit(self, record):
        self.logs.append((record.levelname, record.getMessage(), record.name))


class TestCliLogRunner(unittest.TestCase):

    def test(self):
        handler = DummyLogHandler()
        runner = LogRunner('mock_module', 'LoggingScraper', log_handler=handler, log_verbosity=3, test_logs=[
            {'level': logging.ERROR, 'msg': 'ERROR!'},
        ])
        self.assertEqual('ok_LoggingScraper', runner.run())
        self.assertEqual([
            ('ERROR', 'ERROR!', 'mock_module.scrapers(LoggingScraper)'),
            ('INFO', '_getTitle', 'mock_module.scrapers(LoggingScraper)'),
        ], handler.logs)

    def testOnlyErrors(self):
        handler = DummyLogHandler()
        runner = LogRunner('mock_module', 'LoggingScraper', log_handler=handler, log_verbosity=0, test_logs=[
            {'level': logging.ERROR, 'msg': 'ERROR!'},
        ])
        self.assertEqual('ok_LoggingScraper', runner.run())
        self.assertEqual([
            ('ERROR', 'ERROR!', 'mock_module.scrapers(LoggingScraper)'),
        ], handler.logs)

    def testException(self):
        handler = DummyLogHandler()
        runner = LogRunner('mock_module', 'LoggingScraper', log_handler=handler, fake_error=True, catch_errors=True)
        self.assertEqual(None, runner.run())
        self.assertEqual(1, len(handler.logs))
        self.assertEqual('ERROR', handler.logs[0][0])
        self.assertTrue(handler.logs[0][1].startswith('Traceback (most recent call last):'))
        self.assertEqual('okscraper.cli.runner(LogRunner)', handler.logs[0][2])

class DummyDbLogRunner(DbLogRunner):

    def post_init(self):
        self.dblogs = []

    def on_dblog_emit(self, record):
        """@type record: logging.Record"""
        self.dblogs.append((record.levelname, record.getMessage(), record.name))

    def post_run(self):
        self.committed_dblogs = self.dblogs

class TestCliDbLogRunner(unittest.TestCase):

    def test(self):
        handler = DummyLogHandler()
        runner = DummyDbLogRunner('mock_module', 'LoggingScraper', log_handler=handler, log_verbosity=0, test_logs=[
            {'level': logging.ERROR, 'msg': 'ERROR!'},
            {'level': logging.DEBUG, 'msg': 'DEBUG'},
        ])
        self.assertEqual('ok_LoggingScraper', runner.run())
        # the normal handler only shows errors
        self.assertEqual([
            ('ERROR', 'ERROR!', 'mock_module.scrapers(LoggingScraper)'),
        ], handler.logs)
        # the db log handler shows info as well, but no debug
        self.assertEqual([
            ('ERROR', 'ERROR!', 'mock_module.scrapers(LoggingScraper)'),
            ('INFO', '_getTitle', 'mock_module.scrapers(LoggingScraper)'),
        ], runner.committed_dblogs)

    def testException(self):
        handler = DummyLogHandler()
        runner = DummyDbLogRunner('mock_module', 'LoggingScraper', log_handler=handler, log_verbosity=0, fake_error=True, catch_errors=True)
        self.assertEqual(None, runner.run())
        # the normal handler only shows errors
        self.assertEqual(1, len(handler.logs))
        self.assertEqual('ERROR', handler.logs[0][0])
        self.assertTrue(handler.logs[0][1].startswith('Traceback (most recent call last):'))
        self.assertEqual('testCli(DummyDbLogRunner)', handler.logs[0][2])
        # the db log handler should be the same as db logs - because there is only the single error
        self.assertEqual(handler.logs, runner.committed_dblogs)