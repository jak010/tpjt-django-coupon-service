from unittest import TextTestResult

from django.test.runner import DiscoverRunner, PDBDebugResult
import unittest


class CustomTextTestResult(unittest.TextTestResult):
    def startTest(self, test):
        super(TextTestResult, self).startTest(test)
        if self.showAll:
            if test._testMethodDoc is None:
                raise Exception(f"테스트 문서를 작성해주세요 : target={test._testMethodName}")

            self.stream.write(test._testMethodDoc)
            self.stream.write(" ... ")
            self.stream.flush()
            self._newline = False


class ApplicationTestRunner(DiscoverRunner):
    """ 테스트 실행 시, 기존에 연결된 Dev DB를 통해 테스트할 수 있도록 추가됨 """

    def get_test_runner_kwargs(self):
        return {
            "failfast": self.failfast,
            "resultclass": CustomTextTestResult,
            "verbosity": self.verbosity,
            "buffer": self.buffer,
        }

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
