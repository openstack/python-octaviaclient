#    Copyright 2015
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import testtools

from oslotest import base

from octaviaclient.hacking import checks


class HackingTestCase(base.BaseTestCase):
    """Hacking test class.

    This class tests the hacking checks in octaviaclient.hacking.checks by
    passing strings to the check methods like the pep8/flake8 parser would. The
    parser loops over each line in the file and then passes the parameters to
    the check method. The parameter names in the check method dictate what type
    of object is passed to the check method. The parameter types are::

        logical_line: A processed line with the following modifications:
            - Multi-line statements converted to a single line.
            - Stripped left and right.
            - Contents of strings replaced with "xxx" of same length.
            - Comments removed.
        physical_line: Raw line of text from the input file.
        lines: a list of the raw lines from the input file
        tokens: the tokens that contribute to this logical line
        line_number: line number in the input file
        total_lines: number of lines in the input file
        blank_lines: blank lines before this one
        indent_char: indentation character in this file (" " or "\t")
        indent_level: indentation (with tabs expanded to multiples of 8)
        previous_indent_level: indentation on previous line
        previous_logical: previous logical line
        filename: Path of the file being run through pep8

    When running a test on a check method the return will be False/None if
    there is no violation in the sample input. If there is an error a tuple is
    returned with a position in the line, and a message. So to check the result
    just assertTrue if the check is expected to fail and assertFalse if it
    should pass.
    """

    def assertLinePasses(self, func, *args):
        with testtools.ExpectedException(StopIteration):
            next(func(*args))

    def assertLineFails(self, func, *args):
        self.assertIsInstance(next(func(*args)), tuple)

    def test_no_mutable_default_args(self):
        self.assertEqual(0, len(list(checks.no_mutable_default_args(
            "def foo (bar):"))))
        self.assertEqual(1, len(list(checks.no_mutable_default_args(
            "def foo (bar=[]):"))))
        self.assertEqual(1, len(list(checks.no_mutable_default_args(
            "def foo (bar={}):"))))

    def test_assert_equal_true_or_false(self):
        self.assertEqual(1, len(list(checks.assert_equal_true_or_false(
            "self.assertEqual(True, A)"))))

        self.assertEqual(1, len(list(checks.assert_equal_true_or_false(
            "self.assertEqual(False, A)"))))

        self.assertEqual(0, len(list(checks.assert_equal_true_or_false(
            "self.assertTrue()"))))

        self.assertEqual(0, len(list(checks.assert_equal_true_or_false(
            "self.assertFalse()"))))

    def test_no_log_warn(self):
        self.assertEqual(1, len(list(checks.no_log_warn(
            "LOG.warn()"))))

        self.assertEqual(0, len(list(checks.no_log_warn(
            "LOG.warning()"))))

    def test_no_xrange(self):
        self.assertEqual(1, len(list(checks.no_xrange(
            "xrange(45)"))))

        self.assertEqual(0, len(list(checks.no_xrange(
            "range(45)"))))

    def test_no_log_translations(self):
        for log in checks._all_log_levels:
            for hint in checks._all_hints:
                bad = 'LOG.%s(%s("Bad"))' % (log, hint)
                self.assertEqual(
                    1, len(list(checks.no_translate_logs(bad, 'f'))))
                # Catch abuses when used with a variable and not a literal
                bad = 'LOG.%s(%s(msg))' % (log, hint)
                self.assertEqual(
                    1, len(list(checks.no_translate_logs(bad, 'f'))))
                # Do not do validations in tests
                ok = 'LOG.%s(_("OK - unit tests"))' % log
                self.assertEqual(
                    0, len(list(checks.no_translate_logs(ok, 'f/tests/f'))))

    def test_check_localized_exception_messages(self):
        f = checks.check_raised_localized_exceptions
        self.assertLineFails(f, "     raise KeyError('Error text')", '')
        self.assertLineFails(f, ' raise KeyError("Error text")', '')
        self.assertLinePasses(f, ' raise KeyError(_("Error text"))', '')
        self.assertLinePasses(f, ' raise KeyError(_ERR("Error text"))', '')
        self.assertLinePasses(f, " raise KeyError(translated_msg)", '')
        self.assertLinePasses(f, '# raise KeyError("Not translated")', '')
        self.assertLinePasses(f, 'print("raise KeyError("Not '
                                 'translated")")', '')

    def test_check_localized_exception_message_skip_tests(self):
        f = checks.check_raised_localized_exceptions
        self.assertLinePasses(f, "raise KeyError('Error text')",
                              'neutron_lib/tests/unit/mytest.py')

    def test_check_no_basestring(self):
        self.assertEqual(1, len(list(checks.check_no_basestring(
            "isinstance('foo', basestring)"))))

        self.assertEqual(0, len(list(checks.check_no_basestring(
            "isinstance('foo', six.string_types)"))))

    def test_check_no_eventlet_imports(self):
        f = checks.check_no_eventlet_imports
        self.assertLinePasses(f, 'from not_eventlet import greenthread')
        self.assertLineFails(f, 'from eventlet import greenthread')
        self.assertLineFails(f, 'import eventlet')

    def test_line_continuation_no_backslash(self):
        results = list(checks.check_line_continuation_no_backslash(
            '', [(1, 'import', (2, 0), (2, 6), 'import \\\n'),
                 (1, 'os', (3, 4), (3, 6), '    os\n')]))
        self.assertEqual(1, len(results))
        self.assertEqual((2, 7), results[0][0])
