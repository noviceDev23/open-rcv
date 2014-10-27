
from argparse import ArgumentParser
import os

from openrcv.scripts.argparse import ArgParser, HelpRequested, UsageException
from openrcv.scripts.argparser import create_argparser, get_log_level
from openrcv.utiltest.helpers import skipIfTravis, UnitCase


# TODO: add a test for good args.
class ModuleTestCase(UnitCase):

    def call_get_log_level(self, parser, args):
        return get_log_level(parser, args, default=35)

    @skipIfTravis()
    def test_get_log_level(self):
        parser = create_argparser()
        self.assertEqual(self.call_get_log_level(parser, ['input_path', '--log-level', 'DEBUG']), 10)
        # Check what would otherwise be a UsageException.
        with self.assertRaises(UsageException):
            parser.parse_args([])
        self.assertEqual(self.call_get_log_level(parser, []), 35)
        # Check an unrecognized string.
        self.assertEqual(self.call_get_log_level(parser, ['input_path', '--log-level', 'FOO']), 35)
        # Check not passing the --log-level option.
        self.assertEqual(self.call_get_log_level(parser, ['input_path']), 20)
        # Test what happens if the parser doesn't have a --log-level option.
        parser = ArgumentParser()
        with self.assertRaises(AttributeError):
            self.assertEqual(self.call_get_log_level(parser, []), 40)


class CreateArgparserTestCase(UnitCase):

    """Test create_argparser()."""

    def test_create_argparser(self):
        parser = create_argparser()
        with self.assertRaises(UsageException) as cm:
            parser.parse_args([])
        err = cm.exception
        self.assertEqual(err.args, ('the following arguments are required: INPUT_PATH', ))
        parser = err.parser
        self.assertEqual(type(parser), ArgParser)
        self.assertEqual(parser.prog, "rcv")

    def test_create_argparser__help(self):
        parser = create_argparser()
        with self.assertRaises(HelpRequested):
            parser.parse_args(["--help"])

    # Convenience function so we don't need to pass an input path.
    def parse_args(self, args):
        parser = create_argparser()
        args = ["input_path"] + args
        return parser.parse_args(args)

    def parse_log_level(self, args):
        ns = self.parse_args(args)
        return ns.log_level

    @skipIfTravis()
    def test_log_level(self):
        # Test the default.
        self.assertEqual(self.parse_log_level([]), 20)
        # Test a number.
        self.assertEqual(self.parse_log_level(['--log-level', '15']), 15)
        # Test a string.
        self.assertEqual(self.parse_log_level(['--log-level', 'DEBUG']), 10)
        # Test missing value.
        with self.assertRaises(UsageException):
            self.parse_log_level(['--log-level'])
        # Test invalid value.
        with self.assertRaises(UsageException):
            self.parse_log_level(['--log-level', 'foo'])