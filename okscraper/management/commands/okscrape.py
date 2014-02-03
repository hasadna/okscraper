# encoding: utf-8

from django.core.management.base import BaseCommand
from okscraper.cli.runner import Runner as OkscraperCliRunner
import logging

class Command(BaseCommand):

    args = 'module [class] [arg]..'

    option_list = BaseCommand.option_list + ()

    def _define_logger(self, verbosity):
        logger = logging.getLogger()
        ch = logging.StreamHandler()
        if verbosity == '1':
            level = logging.WARN
        elif verbosity == '2':
            level = logging.INFO
        elif verbosity == '3':
            level = logging.DEBUG
        else:
            level = logging.ERROR
        ch.setLevel(level)
        logger.addHandler(ch)

    def handle(self, *args, **options):
        self._define_logger(options.get('verbosity', '1'))
        runner = OkscraperCliRunner(
            args[0],
            args[1] if len(args)>1 else None,
            *args[2:] if len(args)>2 else []
        )
        runner.run()
