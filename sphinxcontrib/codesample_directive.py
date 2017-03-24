# -*- coding: utf-8 -*-
"""Sphinx directive to display and execute Python code.

This directive accepts Python code, and produces output similar to
docstrings showing interactive sessions, with the "commands" and their
output. The code is executed at documentation build time.

To enable this directive, simply list it in your Sphinx ``conf.py``
file (making sure the directory where you placed it is visible to
sphinx, as is needed for all Sphinx directives). For example::

    extensions = ['sphinxcontrib.codesample_directive']

An example usage of the directive is:

.. code-block:: rst

    .. codesample::

        >>> x = 2
        >>> y = x**2
        >>> print(y)

which produces:

.. code-block:: python

   >>> x = 2
   >>> y = x**2
   >>> print(y)
   4

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
    "A contextmanager to temporarily redirect standard output and error"
    sink = io.StringIO()
    orig = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = sink
    try:
        yield sink
    finally:
        sys.stdout, sys.stderr = orig


SUPPRESS = re.compile(r'#\s*suppress\s*$')

def format_lines(lines):
    for i, line in enumerate(lines):
        if i == 0 and SUPPRESS.search(line):
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
                    'okexcept': directives.flag,
                    'okwarning': directives.flag
                  }

    def run(self):
        globals = {}
        locals = {}

        text = '\n'.join(self.content)
        textlines = text.splitlines()
        tree = ast.parse(text)

        lines = ['.. code-block:: python', '']

        nums = [stmt.lineno for stmt in tree.body]
        nextnums = [min((num for num in nums[i+1:] if num > nums[i]), default=999999)
                    for i in range(len(nums))]
        num = 1

        for i, stmt in enumerate(tree.body):
            # output the code up to the next statement
            if stmt.lineno >= num:
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
