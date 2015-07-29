from unittest import TestCase, mock

import semantic_release
from semantic_release.helpers import get_current_version, get_new_version, upload_to_pypi


class GetCurrentVersionTests(TestCase):

    def test_should_return_correct_version(self):
        self.assertEqual(get_current_version(), semantic_release.__version__)


class GetNewVersionTests(TestCase):

    def test_major_bump(self):
        self.assertEqual(get_new_version('0.0.0', 'major'), '1.0.0')
        self.assertEqual(get_new_version('0.1.0', 'major'), '1.0.0')
        self.assertEqual(get_new_version('0.1.9', 'major'), '1.0.0')
        self.assertEqual(get_new_version('10.1.0', 'major'), '11.0.0')

    def test_minor_bump(self):
        self.assertEqual(get_new_version('0.0.0', 'minor'), '0.1.0')
        self.assertEqual(get_new_version('1.2.0', 'minor'), '1.3.0')
        self.assertEqual(get_new_version('1.2.1', 'minor'), '1.3.0')
        self.assertEqual(get_new_version('10.1.0', 'minor'), '10.2.0')

    def test_patch_bump(self):
        self.assertEqual(get_new_version('0.0.0', 'patch'), '0.0.1')
        self.assertEqual(get_new_version('0.1.0', 'patch'), '0.1.1')
        self.assertEqual(get_new_version('10.0.9', 'patch'), '10.0.10')

    def test_None_bump(self):
        self.assertEqual(get_new_version('1.0.0', None), '1.0.0')


class PypiTests(TestCase):

    @mock.patch('semantic_release.helpers.run')
    def test_upload_without_arguments(self, mock_run):
        upload_to_pypi()
        mock_run.assert_called_once_with('python setup.py bdist_wheel upload && rm -rf build dist')

    @mock.patch('semantic_release.helpers.run')
    def test_upload_with_arguments(self, mock_run):
        upload_to_pypi(dists='sdist')
        mock_run.assert_called_once_with('python setup.py sdist upload && rm -rf build dist')