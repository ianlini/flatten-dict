flatten-dict
============
.. image:: https://github.com/ianlini/flatten-dict/actions/workflows/main.yml/badge.svg
   :target: https://github.com/ianlini/flatten-dict/actions
.. image:: https://img.shields.io/pypi/v/flatten-dict.svg
   :target: https://pypi.org/project/flatten-dict/
.. image:: https://img.shields.io/pypi/l/flatten-dict.svg
   :target: https://github.com/ianlini/flatten-dict/blob/master/LICENSE
.. image:: https://img.shields.io/github/stars/ianlini/flatten-dict.svg?style=social
   :target: https://github.com/ianlini/flatten-dict

A flexible utility for flattening and unflattening dict-like objects in Python.


Introduction
------------
This package provides a function ``flatten()`` for flattening dict-like objects in Python 2.7 and 3.5~3.8.
It also provides some key joining methods (reducer), and you can choose the reducer you want or even implement your own reducer.
You can also invert the resulting flat dict using ``unflatten()``.

Installation
------------

.. code-block:: bash

   pip install flatten-dict

Documentation
-------------

Flatten
```````

.. code-block:: python

   def flatten(d, reducer='tuple', inverse=False, enumerate_types=(), keep_empty_types=()):
       """Flatten `Mapping` object.

       Parameters
       ----------
       d : dict-like object
           The dict that will be flattened.
       reducer : {'tuple', 'path', 'underscore', 'dot', Callable}
           The key joining method. If a `Callable` is given, the `Callable` will be
           used to reduce.
           'tuple': The resulting key will be tuple of the original keys.
           'path': Use `os.path.join` to join keys.
           'underscore': Use underscores to join keys.
           'dot': Use dots to join keys.
       inverse : bool
           Whether you want invert the resulting key and value.
       max_flatten_depth : int
           Maximum depth to merge.
       enumerate_types : Sequence[type]
           Flatten these types using `enumerate`.
           For example, if we set `enumerate_types` to ``(list,)``,
           `list` indices become keys: ``{'a': ['b', 'c']}`` -> ``{('a', 0): 'b', ('a', 1): 'c'}``.
       keep_empty_types : Sequence[type]
           By default, ``flatten({1: 2, 3: {}})`` will give you ``{(1,): 2}``, that is, the key ``3``
           will disappear.
           This is also applied for the types in `enumerate_types`, that is,
           ``flatten({1: 2, 3: []}, enumerate_types=(list,))`` will give you ``{(1,): 2}``.
           If you want to keep those empty values, you can specify the types in `keep_empty_types`:

           >>> flatten({1: 2, 3: {}}, keep_empty_types=(dict,))
           {(1,): 2, (3,): {}}

       Returns
       -------
       flat_dict : dict
       """

Examples
::::::::

>>> from flatten_dict import flatten
>>> from pprint import pprint
>>> normal_dict = {
...     'a': '0',
...     'b': {
...         'a': '1.0',
...         'b': '1.1',
...     },
...     'c': {
...         'a': '2.0',
...         'b': {
...             'a': '2.1.0',
...             'b': '2.1.1',
...         },
...     },
... }
>>> pprint(flatten(normal_dict))
{('a',): '0',
 ('b', 'a'): '1.0',
 ('b', 'b'): '1.1',
 ('c', 'a'): '2.0',
 ('c', 'b', 'a'): '2.1.0',
 ('c', 'b', 'b'): '2.1.1'}
>>> pprint(flatten(normal_dict, reducer='path'))
{'a': '0',
 'b/a': '1.0',
 'b/b': '1.1',
 'c/a': '2.0',
 'c/b/a': '2.1.0',
 'c/b/b': '2.1.1'}
>>> pprint(flatten(normal_dict, reducer='path', inverse=True))
{'0': 'a',
 '1.0': 'b/a',
 '1.1': 'b/b',
 '2.0': 'c/a',
 '2.1.0': 'c/b/a',
 '2.1.1': 'c/b/b'}
>>> pprint(flatten(normal_dict, reducer='path', max_flatten_depth=2))
{'a': '0',
 'b/a': '1.0',
 'b/b': '1.1',
 'c/a': '2.0',
 'c/b': {'a': '2.1.0', 'b': '2.1.1'}}

The `reducer` parameter supports ``'tuple'``, ``'path'``, ``'underscore'``, ``'dot'`` and `Callable`. We can customize the reducer using a function:

>>> def underscore_reducer(k1, k2):
...     if k1 is None:
...         return k2
...     else:
...         return k1 + "_" + k2
...
>>> pprint(flatten(normal_dict, reducer=underscore_reducer))
{'a': '0',
 'b_a': '1.0',
 'b_b': '1.1',
 'c_a': '2.0',
 'c_b_a': '2.1.0',
 'c_b_b': '2.1.1'}

There is also a factory function `make_reducer()` to help you create customized reducer. The function currently only supports customized delimiter:

>>> from flatten_dict.reducers import make_reducer
>>> pprint(flatten(normal_dict, reducer=make_reducer(delimiter='_')))
{'a': '0',
 'b_a': '1.0',
 'b_b': '1.1',
 'c_a': '2.0',
 'c_b_a': '2.1.0',
 'c_b_b': '2.1.1'}

If we have some iterable (e.g., `list`) in the `dict`, we will normally get this:

>>> flatten({'a': [1, 2, 3], 'b': 'c'})
{('a',): [1, 2, 3], ('b',): 'c'}

If we want to use its indices as keys, then we can use the parameter `enumerate_types`:

>>> flatten({'a': [1, 2, 3], 'b': 'c'}, enumerate_types=(list,))
{('a', 0): 1, ('a', 1): 2, ('a', 2): 3, ('b',): 'c'}

We can even flatten a `list` directly:

>>> flatten([1, 2, 3], enumerate_types=(list,))
{(0,): 1, (1,): 2, (2,): 3}

If there is an empty dict in the values, by default, it will disappear after flattened:

>>> flatten({1: 2, 3: {}})
{(1,): 2}

We can keep the empty dict in the result using ``keep_empty_types=(dict,)``:

>>> flatten({1: 2, 3: {}}, keep_empty_types=(dict,))
{(1,): 2, (3,): {}}

Unflatten
`````````

.. code-block:: python

   def unflatten(d, splitter='tuple', inverse=False):
       """Unflatten dict-like object.

       Parameters
       ----------
       d : dict-like object
           The dict that will be unflattened.
       splitter : {'tuple', 'path', 'underscore', 'dot', Callable}
           The key splitting method. If a Callable is given, the Callable will be
           used to split `d`.
           'tuple': Use each element in the tuple key as the key of the unflattened dict.
           'path': Use `pathlib.Path.parts` to split keys.
           'underscore': Use underscores to split keys.
           'dot': Use underscores to split keys.
       inverse : bool
           Whether you want to invert the key and value before flattening.

       Returns
       -------
       unflattened_dict : dict
       """

Examples
::::::::

>>> from pprint import pprint
>>> from flatten_dict import unflatten
>>> flat_dict = {
...     ('a',): '0',
...     ('b', 'a'): '1.0',
...     ('b', 'b'): '1.1',
...     ('c', 'a'): '2.0',
...     ('c', 'b', 'a'): '2.1.0',
...     ('c', 'b', 'b'): '2.1.1',
... }
>>> pprint(unflatten(flat_dict))
{'a': '0',
 'b': {'a': '1.0', 'b': '1.1'},
 'c': {'a': '2.0', 'b': {'a': '2.1.0', 'b': '2.1.1'}}}
>>> flat_dict = {
...     'a': '0',
...     'b/a': '1.0',
...     'b/b': '1.1',
...     'c/a': '2.0',
...     'c/b/a': '2.1.0',
...     'c/b/b': '2.1.1',
... }
>>> pprint(unflatten(flat_dict, splitter='path'))
{'a': '0',
 'b': {'a': '1.0', 'b': '1.1'},
 'c': {'a': '2.0', 'b': {'a': '2.1.0', 'b': '2.1.1'}}}
>>> flat_dict = {
...     '0': 'a',
...     '1.0': 'b/a',
...     '1.1': 'b/b',
...     '2.0': 'c/a',
...     '2.1.0': 'c/b/a',
...     '2.1.1': 'c/b/b',
... }
>>> pprint(unflatten(flat_dict, splitter='path', inverse=True))
{'a': '0',
 'b': {'a': '1.0', 'b': '1.1'},
 'c': {'a': '2.0', 'b': {'a': '2.1.0', 'b': '2.1.1'}}}

The `splitter` parameter supports ``'tuple'``, ``'path'``, ``'underscore'``, ``'dot'`` and `Callable`. We can customize the reducer using a function:

>>> def underscore_splitter(flat_key):
...     return flat_key.split("_")
...
>>> flat_dict = {
...     'a': '0',
...     'b_a': '1.0',
...     'b_b': '1.1',
...     'c_a': '2.0',
...     'c_b_a': '2.1.0',
...     'c_b_b': '2.1.1',
... }
>>> pprint(unflatten(flat_dict, splitter=underscore_splitter))
{'a': '0',
 'b': {'a': '1.0', 'b': '1.1'},
 'c': {'a': '2.0', 'b': {'a': '2.1.0', 'b': '2.1.1'}}}

There is also a factory function `make_splitter()` to help you create customized splitter. The function currently only supports customized delimiter:

>>> from flatten_dict.splitters import make_splitter
>>> pprint(unflatten(flat_dict, splitter=make_splitter(delimiter='_')))
{'a': '0',
 'b': {'a': '1.0', 'b': '1.1'},
 'c': {'a': '2.0', 'b': {'a': '2.1.0', 'b': '2.1.1'}}}
