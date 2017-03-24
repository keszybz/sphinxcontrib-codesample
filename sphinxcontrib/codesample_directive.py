# -*- coding: utf-8 -*-
"""Sphinx directive to display and execute Python code.

This directive accepts Python code, and produces output similar to
docstrings showing interactive sessions, with the "commands" and their
output. The code is executed at documentation build time.

To enable this directive, simply list it in your Sphinx ``conf.py``
file (making sure the directory where you placed it is visible to
sphinx, as is needed for all Sphinx directives). For example::

    extensions = ['sphinxcontrib.codesample_directive']

Options that can be placed in conf.py are:

suppress:
   Do not print the code statements, just their output.
   Needs a boolean value.

Options that can be specified for each block:

suppress:
   Do not print the code statements, just their output.

nosuppress:
   Reverses `suppress` specified globally.

Special comments:

SUPPRESS:
   Do not print the code statements, just their output.

An example usage of the directive is:

.. code-block:: rst

    .. codesample::

        x = 2
        y = x**2
        y += 1                 # SUPPRESS
        print(y)

which produces:

.. code-block:: python

   >>> x = 2
   >>> y = x**2
   >>> print(y)                # doctest: +SKIP
   5

"""

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Stdlib
import ast
import contextlib
import io
import os
import sys
import re

# Third-party
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive

#-----------------------------------------------------------------------------
# Functions and class declarations
#-----------------------------------------------------------------------------

@contextlib.contextmanager
def capture_stdout_stderr():
    r"""A context manager to temporarily redirect standard output and error

    >>> with capture_stdout_stderr() as sink:
    ...   print('foobar')
    >>> sink.getvalue()
    'foobar\n'
    """
    sink = io.StringIO()
    orig = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = sink
    try:
        yield sink
    finally:
        sys.stdout, sys.stderr = orig


SUPPRESS = re.compile(r'#\s*SUPPRESS\s*$')

def format_lines(lines):
    r"""Add >>>/... prompts to lines as if the were typed interactively

    >>> s = '''\
    ... x = (3
    ... + 5)'''.splitlines()
    >>> print(s)
    ['x = (3', '+ 5)']
    >>> list(format_lines(s))
    ['   >>> x = (3', '   ... + 5)']
    """
    for i, line in enumerate(lines):
        if SUPPRESS.search(line):
            break
        if line:
            yield '   {} {}'.format('>>>' if i == 0 else '...', line)
        elif any(lines[i+1:]):
            yield '   ...'
        else:
            # skip the ellipsis for the empty lines at end
            yield '   '

class CodesampleDirective(Directive):

    has_content = True
    required_arguments = 0
    optional_arguments = 1 # filename
    final_argumuent_whitespace = True
    option_spec = { 'suppress' : directives.flag,
                    'nosuppress' : directives.flag,
                    'okexcept': directives.flag,
                    'okwarning': directives.flag
                  }

    @staticmethod
    def codesample_option(name):
        return 'codesample_' + name

    def getoption(self, name):
        if name in self.options:
            return True
        if 'no' + name in self.options:
            return False

        config = self.state.document.settings.env.config
        return getattr(config, self.codesample_option(name))

    def run(self):
        globals = {}
        locals = {}

        suppress = self.getoption('suppress')

        text = '\n'.join(self.content)
        textlines = text.splitlines()
        tree = ast.parse(text)

        lexer = 'python' if not suppress else 'text'
        lines = ['.. code-block:: {}'.format(lexer), '']

        nums = [stmt.lineno for stmt in tree.body]
        nextnums = [min((num for num in nums[i+1:] if num > nums[i]), default=999999)
                    for i in range(len(nums))]
        num = 1

        for i, stmt in enumerate(tree.body):
            if stmt.lineno >= num and not suppress:
                # output the code up to the next statement
                batch = format_lines(textlines[num-1:nextnums[i]-1])
                lines.extend(batch)
                num = nextnums[i]

            source = ast.Interactive([stmt])
            module = compile(source, '<block>', 'single')
            with capture_stdout_stderr() as capture:
                exec(module, globals, locals)
            lines.extend('   {}'.format(line)
                         for line in capture.getvalue().splitlines())

        self.state_machine.insert_input(
            lines, self.state_machine.input_lines.source(0))

        return []

# Enable as a proper Sphinx directive
def setup(app):
    setup.app = app

    app.add_directive('codesample', CodesampleDirective)
    app.add_config_value(CodesampleDirective.codesample_option('suppress'),
                         None, 'env')
