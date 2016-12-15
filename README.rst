flatten-dict
============
.. image:: https://img.shields.io/travis/ianlini/flatten-dict/master.svg
   :target: https://travis-ci.org/ianlini/flatten-dict
.. image:: https://img.shields.io/pypi/v/flatten-dict.svg
   :target: https://pypi.python.org/pypi/flatten-dict
.. image:: https://img.shields.io/pypi/l/flatten-dict.svg
   :target: https://pypi.python.org/pypi/flatten-dict

A flexible utility for flattening dict-like objects in Python.


Introduction
------------
This Python package provide a function ``flatten()`` for flattening dict-like objects.
It also provides some key joining methods (reducer), and you can choose the reducer you want or even implement your own reducer. You can also choose to invert the resulting flat dict.

Documentation
-------------

.. code-block:: python

   def flatten(d, reducer='tuple', inverse=False):
       """Flatten dict-like object.

       Parameters
       ----------
       d: dict-like object
           The dict that will be flattened.
       reducer: {'tuple', 'path', function} (default: 'tuple')
           The key joining method. If a function is given, the function will be
           used to reduce.
           'tuple': The resulting key will be tuple of the original keys
           'path': Use ``os.path.join`` to join keys.
       inverse: bool (default: False)
           Whether you want invert the resulting key and value.

       Returns
       -------
       flat_dict: dict
       """


Examples
--------
.. code-block:: python

   In [1]: from flatten_dict import flatten

   In [2]: normal_dict = {
      ...:     'a': '0',
      ...:     'b': {
      ...:         'a': '1.0',
      ...:         'b': '1.1',
      ...:     },
      ...:     'c': {
      ...:         'a': '2.0',
      ...:         'b': {
      ...:             'a': '2.1.0',
      ...:             'b': '2.1.1',
      ...:         },
      ...:     },
      ...: }

   In [3]: flatten(normal_dict)
   Out[3]:
   {('a',): '0',
    ('b', 'a'): '1.0',
    ('b', 'b'): '1.1',
    ('c', 'a'): '2.0',
    ('c', 'b', 'a'): '2.1.0',
    ('c', 'b', 'b'): '2.1.1'}

   In [4]: flatten(normal_dict, reducer='path')
   Out[4]:
   {'a': '0',
    'b/a': '1.0',
    'b/b': '1.1',
    'c/a': '2.0',
    'c/b/a': '2.1.0',
    'c/b/b': '2.1.1'}

   In [5]: flatten(normal_dict, reducer='path', inverse=True)
   Out[5]:
   {'0': 'a',
    '1.0': 'b/a',
    '1.1': 'b/b',
    '2.0': 'c/a',
    '2.1.0': 'c/b/a',
    '2.1.1': 'c/b/b'}

   In [6]: def underscore_reducer(k1, k2):
      ...:     if k1 is None:
      ...:         return k2
      ...:     else:
      ...:         return k1 + "_" + k2
      ...:

   In [7]: flatten(normal_dict, reducer=underscore_reducer)
   Out[7]:
   {'a': '0',
    'b_a': '1.0',
    'b_b': '1.1',
    'c_a': '2.0',
    'c_b_a': '2.1.0',
    'c_b_b': '2.1.1'}
