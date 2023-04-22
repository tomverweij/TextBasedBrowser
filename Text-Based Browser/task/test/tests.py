from hstest.stage_test import *
import requests
import os
import shutil
import sys

if sys.platform.startswith("win"):
    import _locale

    # pylint: disable=protected-access
    _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)

names = {'bloomberg': 'bloomberg.com',
         'docs': 'docs.python.org',
         'nytimes': 'nytimes.com'
         }


class TextBasedBrowserTest(StageTest):

    def generate(self):

        dir_for_files = 'tb_tabs'
        return [
            TestCase(
                stdin='docs.python.org\nexit',
                attach='docs.python.org',
                args=[dir_for_files]
            ),
            TestCase(
                stdin='nytimescom\nexit',
                attach=None,
                args=[dir_for_files]
            ),
            TestCase(
                stdin='back\nexit',
                attach='back',
                args=['tb_tabs']
            ),
            TestCase(
                stdin='peps.python.org/pep-0008/\ndocs.python.org\npeps\nexit',
                attach=('peps.python.org/pep-0008/', 'docs.python.org', 'peps.python.org/pep-0008/'),
                args=[dir_for_files]
            ),
            TestCase(
                stdin='peps.python.org/pep-0008/\ndocs.python.org\nback\nexit',
                attach=('peps.python.org/pep-0008/', 'docs.python.org', 'docs.python.org'),
                args=['tb_tabs']
            )
        ]

    def compare_pages(self, output_page, ideal_page):
        ideal_page = ideal_page.split('\n')
        for line in ideal_page:
            if line.strip() not in output_page:
                return False, line.strip()
        return True, ""

    def _check_files(self, path_for_tabs: str, ideal_page: str, attach: str):
        """
        Helper which checks that browser saves visited url in files and
        provides access to them.

        :param path_for_tabs: directory which must contain saved tabs
        :param ideal_page: HTML code of the needed page
        """

        path, dirs, filenames = next(os.walk(path_for_tabs))

        name = attach.split('.')[0]
        if name in filenames:
            print("found file: {}".format(name))
            with open(os.path.join(path_for_tabs, name), 'r', encoding='utf-8') as tab:
                try:
                    content = tab.read()
                except UnicodeDecodeError:
                    raise WrongAnswer('An error occurred while reading your saved tab. '
                                      'Perhaps you used the wrong encoding?')
                is_page_saved_correctly, wrong_line = self.compare_pages(content, ideal_page)
                if not is_page_saved_correctly:
                    raise WrongAnswer(f"The following line is missing from the file {name}:\n"
                                      f"\'{wrong_line}\'\n"
                                      f"Make sure you output the needed web page to the file\n"
                                      f"and save the file in the utf-8 encoding.")
        else:
            raise WrongAnswer(f"Couldn't find file with the name {name}.\n"
                              f"Make sure you saved the tab and named it correctly.")

    @staticmethod
    def get_page(url):

        url = f'https://{url}'
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/70.0.3538.77 Safari/537.36"
        try:
            page = requests.get(url, headers={'User-Agent': user_agent})
        except requests.exceptions.ConnectionError:
            raise WrongAnswer(f"An error occurred while tests tried to connect to the page {url}.\n"
                              f"Please try again a bit later.")
        return page.text

    def check_correct_url(self, attach_0: str, path_for_tabs: str, reply):

        ideal_page = TextBasedBrowserTest.get_page(attach_0)
        self._check_files(path_for_tabs, ideal_page, attach_0)

        is_page_printed_correctly, wrong_line = self.compare_pages(reply, ideal_page)
        if not is_page_printed_correctly:
            return CheckResult.wrong(f"The following line in missing from your console output:\n"
                                     f"\'{wrong_line}\'\n"
                                     f"Make sure you output the needed web page to the console.")

    def check(self, reply, attach):

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
        path_for_tabs = os.path.join(os.curdir, 'tb_tabs')

        if not os.path.isdir(path_for_tabs):
            return CheckResult.wrong("There is no directory for tabs")

        if isinstance(attach, str):
            attach_0 = attach
            self.check_correct_url(attach_0, path_for_tabs, reply)

        if isinstance(attach, tuple):
            for element in attach:
                attach_0 = element
                self.check_correct_url(attach_0, path_for_tabs, reply)

        try:
            shutil.rmtree(path_for_tabs)
        except PermissionError:
            return CheckResult.wrong("Impossible to remove the directory for tabs. \n"
                                     "Perhaps you haven't closed some file?")

        return CheckResult.correct()


if __name__ == '__main__':
    TextBasedBrowserTest().run_tests()
