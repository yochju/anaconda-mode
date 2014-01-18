from unittest import TestCase
from start_jedi import jedi
import os


class TestJedi(TestCase):

    def test_unsupported_command(self):
        """Should raise exception on adjective command requests."""

        request = {
            'command': 'some_strange_command',
            'attributes': {
                'source': '''\nimport datetime\ndatetime.da''',
                'line': 3,
                'column': 14,
                'point': 28,
                'path': '',
                'company_prefix': '',
                'company_arg': ''
            }
        }

        self.assertIsNone(jedi.process(**request))

    def test_missing_attributes(self):
        """Should raise exception on incomplete source code."""

        request = {
            'command': 'candidates',
            'attributes': {}
        }

        self.assertIsNone(jedi.process(**request))

    def test_references_search(self):
        """Jedi must find all references to object."""

        request = {
            'command': 'reference',
            'attributes': {
                'source': '''
def a(t):
    return t

m = a(1)
v = a('b')''',
                'line': 2,
                'column': 4,
                'point': 5,
                'path': 'example.py',
                'company_prefix': '',
                'company_arg': ''
            }
        }

        response = {
            os.getcwd() + '/example.py:5 - a@5,4': {
                'module_path': os.getcwd() + '/example.py',
                'line': 5,
                'column': 4,
                'description': 'a@5,4'
            },
            os.getcwd() + '/example.py:6 - a@6,4': {
                'module_path': os.getcwd() + '/example.py',
                'line': 6,
                'column': 4,
                'description': 'a@6,4'
            }
        }

        self.assertEqual(response, jedi.process(**request))

    def test_empty_references(self):
        """Strip unknown references."""

        request = {
            'command': 'reference',
            'attributes': {
                'source': '''
def a(t):
    return t''',
                'line': 2,
                'column': 4,
                'point': 5,
                'path': 'example.py',
                'company_prefix': '',
                'company_arg': ''
            }
        }

        self.assertIsNone(jedi.process(**request))

    def test_documentation_search(self):
        """Jedi must find all assignments documentation."""

        request = {
            'command': 'doc',
            'attributes': {
                'source': '''
def f(a, b=1):
    "Document for function f."
    pass''',
                'line': 2,
                'column': 4,
                'point': 5,
                'path': 'example.py',
                'company_prefix': '',
                'company_arg': ''
            }
        }

        response = {'Document for function f.': 'Document for function f.'}

        self.assertEqual(response, jedi.process(**request))

    def test_empty_documentation(self):
        """Ignore docless functions."""

        request = {
            'command': 'doc',
            'attributes': {
                'source': '''def ttt(a, b, c):
    pass

ttt''',
                'line': 4,
                'column': 3,
                'point': 31,
                'path': 'simple.py',
                'company_prefix': '',
                'company_arg': ''
            }
        }

        self.assertIsNone(jedi.process(**request))

    def test_short_documentation_search(self):
        """Jedi must find all short documentations."""

        request = {
            'command': 'meta',
            'attributes': {
                'source': '''
def f(a, b=1):
    """Document for function f.

Here is long f function description."""
    pass''',
                'line': 2,
                'column': 4,
                'point': 5,
                'path': 'example.py',
                'company_prefix': '',
                'company_arg': ''
            }
        }

        response = 'Document for function f.'

        self.assertEqual(response, jedi.process(**request))

    def test_empty_meta(self):
        """Ignore docless functions."""

        request = {
            'command': 'meta',
            'attributes': {
                'source': '''def ttt(a, b, c):
    pass

ttt''',
                'line': 4,
                'column': 3,
                'point': 31,
                'path': 'simple.py',
                'company_prefix': '',
                'company_arg': ''
            }
        }

        self.assertIsNone(jedi.process(**request))

    def test_eldoc(self):
        """Should return signature string."""

        request = {
            'command': 'eldoc',
            'attributes': {
                'source': '''
import json
json.dump()''',
                'line': 3,
                'column': 10,
                'point': 25,
                'path': 'example.py',
                'company_prefix': '',
                'company_arg': ''
            }
        }

        response = ("dump(obj, fp, skipkeys = False, ensure_ascii = True, "
                    "check_circular = True, allow_nan = True, cls = None, "
                    "indent = None, separators = None, default = None, "
                    "sort_keys = False, **kw)")

        self.assertEqual(response, jedi.process(**request))

    def test_empty_eldoc(self):
        """Don't answer eldoc on unknown functions."""

        request = {
            'command': 'eldoc',
            'attributes': {
                'source': '''def a:
    pass

z = a()''',
                'line': 4,
                'column': 6,
                'point': 23,
                'path': 'example.py',
                'company_prefix': '',
                'company_arg': ''
            }
        }

        self.assertIsNone(jedi.process(**request))
