examples = ('''\
x = 2
y = x**2
y += 1                 # SUPPRESS
print(y)
''',

'''\
def f(a=3):
    return a ** 3

print(f)
print(f(3))
''')

from sphinxcontrib.codesample_directive import CodesampleDirective

import pytest

@pytest.mark.parametrize("block", examples)
@pytest.mark.parametrize("suppress", (False, True, None))
def test_basic(block, suppress):
    options = {}
    if suppress is not None:
        options['suppress'] = suppress

    content = block.split('\n')

    CodesampleDirective('debug', arguments=None, options=options,
                          content=content, lineno=0,
                          content_offset=None, block_text=None,
                          state=None, state_machine=None)
