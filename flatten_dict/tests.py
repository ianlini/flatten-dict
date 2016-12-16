from __future__ import absolute_import

import six
from nose.tools import assert_raises

from flatten_dict import flatten
from flatten_dict.reducer import tuple_reducer


normal_dict = {
    'a': '0',
    'b': {
        'a': '1.0',
        'b': '1.1',
    },
    'c': {
        'a': '2.0',
        'b': {
            'a': '2.1.0',
            'b': '2.1.1',
        },
    },
}

flat_normal_dict = {
    ('a',): '0',
    ('b', 'a'): '1.0',
    ('b', 'b'): '1.1',
    ('c', 'a'): '2.0',
    ('c', 'b', 'a'): '2.1.0',
    ('c', 'b', 'b'): '2.1.1',
}


def test_flatten_dict():
    assert flatten(normal_dict) == flat_normal_dict

def test_flatten_dict_inverse():
    inv_flat_normal_dict = {v: k for k, v in six.viewitems(flat_normal_dict)}
    assert flatten(normal_dict, inverse=True) == inv_flat_normal_dict

def test_flatten_dict_with_reducer():
    assert flatten(normal_dict, reducer=tuple_reducer) == flat_normal_dict

def test_flatten_dict_path():
    from os.path import join
    flat_path_dict = {join(*k): v for k, v in six.viewitems(flat_normal_dict)}
    assert flatten(normal_dict, reducer='path') == flat_path_dict

def test_flatten_dict_inverse_with_duplicated_value():
    dup_val_dict = normal_dict.copy()
    dup_val_dict['a'] = '2.1.1'
    with assert_raises(ValueError):
        flatten(dup_val_dict, inverse=True)
