import os
import sys

path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sphinxcontrib')
sys.path.insert(0, path)

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'codesample_directive',
]

source_suffix = '.rst'

master_doc = 'index'

# General information about the project.
project = 'codesample_directive'
copyright = '2017, Zbigniew Jędrzejewski-Szmek'
author = 'Zbigniew Jędrzejewski-Szmek'

version = '0.0.0'
release = version

default_role = 'any'

pygments_style = 'sphinx'

todo_include_todos = True

html_theme = 'alabaster'
html_static_path = ['static']

intersphinx_mapping = {'python':('https://docs.python.org/3/', None),
                       'sphinx':('http://www.sphinx-doc.org/en/stable', None),
}
