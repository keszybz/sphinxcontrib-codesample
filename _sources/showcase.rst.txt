Show case
~~~~~~~~~

plain
`````

.. code::

   x = 2
   y = x**2
   print(y)

.. codesample::

   x = 2
   y = x**2
   print(y)

multiline string
````````````````

.. code::

   s = '''
   a b c
   d e f
   '''
   print(s)

.. codesample::

   s = '''
   a b c
   d e f
   '''
   print(s)

multiline function
``````````````````

.. code::

   def f(x, y, *, z=11):
       "Return the frobnication of x, y, and z"
       return x + y + z
   y = f(1, 2, z=3)
   print(y)

.. codesample::

   def f(x, y, *, z=11):
       "Return the frobnication of x, y, and z"
       return x + y + z
   y = f(1, 2, z=3)
   print(y)

suppress inline
```````````````

.. code::

   def ellipsized_function(x, y, *, z=11):
       "Return the frobnication of x, y, and z" # SUPPRESS
       ...
       return x + y + z                         # SUPPRESS
   y = ellipsized_function(1, 2, z=3)                             
   print(y)

.. codesample::

   def ellipsized_function(x, y, *, z=11):
       "Return the frobnication of x, y, and z" # SUPPRESS
       ...
       return x + y + z                         # SUPPRESS
   y = ellipsized_function(1, 2, z=3)                             
   print(y)

suppress block
``````````````

.. code::

   :suppress:

   x = 1
   y = 2
   print('this should be the only line visible')

.. codesample::
   :suppress:

   x = 1
   y = 2
   print('this should be the only line visible')

unsuppress block
````````````````

.. code::

   :nosuppress:

   x = 1
   y = 2
   print('this should be the third line of code')

.. codesample::
   :nosuppress:

   x = 1
   y = 2
   print('this should be the third line of code')
