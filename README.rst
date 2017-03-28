########################
sphinxcontrib-codesample
########################

A Sphinx_ extension to insert arbitrary Python code and its output
into documents. Very similar to code samples in docstrings, but the
output is dynamically generated each time documentation is built.

This extension is similar to IPython's `ipython_directive`_, but does
not use IPython formatting conventions and is much simpler by the
virtue of using plain Python to execute commands.

Installation
------------

Install this extension using pip from `pypi`_::

   pip install sphinxcontrib-codesample

Usage
-----

Just add this extension to ``extensions``::

   extensions = ['sphinxcontrib.codesample']

and insert plain Python code:

.. code-block:: rst

   .. codesample::

      x = 3
      print(x**3)

Output:

.. code-block:: python

   >>> x = 3
   >>> print(x ** 3)
   9

Please refer to the documentation_ for comprehensive information about usage.


Issues
------

Please report issues to the `issue tracker`_ if you found a bug.

Development
-----------

The source code is hosted on github::

   git clone https://github.com/keszybz/sphinxcontrib-codesample

.. _Sphinx: http://sphinx.pocoo.org/latest
.. _ipython_directive: http://matplotlib.org/sampledoc/ipython_directive.html
.. _pypi: http://pypi.python.org/pypi/sphinxcontrib-codesample
.. _documentation: https://sphinxcontrib-codesample.github.io
.. _issue tracker: https://github.com/keszybz/sphinxcontrib-codesample/issues
.. _Github: https://github.com/keszybz/sphinxcontrib-codesample
