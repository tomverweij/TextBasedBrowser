from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult

import os
import shutil

import sys
if sys.platform.startswith("win"):
    import _locale
    # pylint: disable=protected-access
    _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class TextBasedBrowserTest(StageTest):

    def generate(self):
        return [
            TestCase(
                stdin='bloomberg.com\nbloomberg\nexit',
                attach=('Bloomberg', 'New York Times', 'bloomberg'),
                args=['tb_tabs']
            ),
            TestCase(
                stdin='nytimes.com\nnytimes\nexit',
                attach=('New York Times', 'Bloomberg', 'nytimes'),
                args=['tb_tabs']
            ),
            TestCase(
                stdin='nytimescom\nexit',
                args=['tb_tabs']
            ),
            TestCase(
                stdin='blooomberg.com\nexit',
                args=['tb_tabs']
            ),
            TestCase(
                stdin='blooomberg.com\nnytimes.com\nexit',
                attach=(None, 'New York Times', 'Bloomberg', 'nytimes'),
                args=['tb_tabs']
            ),
            TestCase(
                stdin='nytimescom\nbloomberg.com\nexit',
                attach=(None, 'Bloomberg', 'New York Times', 'bloomberg'),
                args=['tb_tabs']
            ),
            TestCase(
                stdin='back\nexit',
                attach='back',
                args=['tb_tabs']
            ),
            TestCase(
                stdin='bloomberg.com\nnytimes.com\nback\nexit',
                attach={
                    'This New Liquid Is Magnetic, and Mesmerizing': (1, 'New York Times'),
                    'The Space Race: From Apollo 11 to Elon Musk': (2, 'Bloomberg')
                },
                args=['tb_tabs']
            ),
            TestCase(
                stdin='nytimes.com\nbloomberg.com\nback\nexit',
                attach={
                    'This New Liquid Is Magnetic, and Mesmerizing': (2, 'New York Times'),
                    'The Space Race: From Apollo 11 to Elon Musk': (1, 'Bloomberg')
                },
                args=['tb_tabs']
            ),
        ]

    def _check_files(self, path_for_tabs: str, right_word: str) -> int:
        """
        Helper which checks that browser saves visited url in files and
        provides access to them.

        :param path_for_tabs: directory which must contain saved tabs
        :param right_word: Word-marker which must be in right tab
        :return: True, if right_words is present in saved tab
        """

        for path, dirs, files in os.walk(path_for_tabs):
            for file in files:
                with open(os.path.join(path_for_tabs, file), 'r') as tab:
                    try:
                        content = tab.read()
                    except UnicodeDecodeError:
                        return -1
                    if right_word in content:
                        return 1
            break

        return 0

    def check(self, reply, attach):

        path_for_tabs = 'tb_tabs'

        # Incorrect URL
        if attach is None:
            if 'invalid url' in reply.lower():
                return CheckResult.correct()
            else:
                return CheckResult.wrong('An invalid URL was input to your program.\n'
                                         'Your program should print \'Invalid URL\'.')

        if attach == 'back':
            if not reply:
                return CheckResult.correct()
            else:
                return CheckResult.wrong(f'There should be no output. But your program printed: {reply}')

        # Correct URL
        if isinstance(attach, tuple):

            if len(attach) == 4:
                _, *attach = attach
                if 'invalid url' not in reply.lower():
                    return CheckResult.wrong('An invalid URL was input to your program.\n'
                                             'Your program should print \'Invalid URL\'.')

            right_word, wrong_word, correct_file_name = attach
            right_word, wrong_word, correct_file_name = attach

            if not os.path.isdir(path_for_tabs):
                return CheckResult.wrong(
                    "Can't find a directory \"" + path_for_tabs + "\" "
                    "in which you should save your web pages.")

            check_files_result = self._check_files(path_for_tabs, right_word)
            if not check_files_result:
                return CheckResult.wrong(
                    "Seems like you didn\'t save the web page "
                    "\"" + right_word + "\" into the "
                    "directory \"" + path_for_tabs + "\". "
                    "This file with page should be named \"" + correct_file_name + "\"")
            elif check_files_result == -1:
                return CheckResult.wrong('An error occurred while reading your saved tab. '
                                         'Perhaps you used the wrong encoding?')

            if wrong_word in reply:
                return CheckResult.wrong('It seems like you printed wrong variable')

            if right_word in reply:
                return CheckResult.correct()

            return CheckResult.wrong('You printed neither bloomberg_com nor nytimes_com')

        if isinstance(attach, dict):
            for key, value in attach.items():
                count, site = value
                real_count = reply.count(key)
                if reply.count(key) != count:
                    return CheckResult.wrong(
                        f'The site "{site}" should be displayed {count} time(s).\n'
                        f'Actually displayed: {real_count} time(s).'
                    )
        try:
            shutil.rmtree(path_for_tabs)
        except PermissionError:
            return CheckResult.wrong(
                "Impossible to remove the directory for tabs. Perhaps you haven't closed some file?")

        return CheckResult.correct()

if __name__ == '__main__':
    TextBasedBrowserTest().run_tests()
