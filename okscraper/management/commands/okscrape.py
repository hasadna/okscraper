# encoding: utf-8

from django.core.management.base import BaseCommand
from optparse import make_option
from okscraper.cli import run, InvalidArgsException
import sys, logging

class Command(BaseCommand):

    args = 'module class args*'

    option_list = BaseCommand.option_list + ()

    def handle(self, *args, **options):
        verbosity = options.get('verbosity', '1')
        if verbosity == '1':
            logging.basicConfig(level=logging.WARN)
        elif verbosity == '2':
            logging.basicConfig(level=logging.INFO)
        elif verbosity == '3':
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.ERROR)

        try:
            run(args)
        except InvalidArgsException:
            print "Invalid arguments\n"
            self.print_help('manage.py', 'okscraper')
