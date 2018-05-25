from __future__ import absolute_import
import os.path

import six
from nose.tools import assert_raises

from flatten_dict import flatten, unflatten
from flatten_dict.reducer import tuple_reducer
from flatten_dict.splitter import tuple_splitter


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
    flat_path_dict = {os.path.join(*k): v for k, v in six.viewitems(flat_normal_dict)}
    assert flatten(normal_dict, reducer='path') == flat_path_dict


def test_flatten_dict_inverse_with_duplicated_value():
    dup_val_dict = normal_dict.copy()
    dup_val_dict['a'] = '2.1.1'
    with assert_raises(ValueError):
        flatten(dup_val_dict, inverse=True)


def test_unflatten_dict():
    assert unflatten(flat_normal_dict) == normal_dict


def test_unflatten_dict_inverse():
    inv_flat_normal_dict = {v: k for k, v in six.viewitems(flat_normal_dict)}
    assert unflatten(inv_flat_normal_dict, inverse=True) == normal_dict


def test_unflatten_dict_path():
    flat_path_dict = {os.path.join(*k): v for k, v in six.viewitems(flat_normal_dict)}
    assert unflatten(flat_path_dict, splitter='path') == normal_dict


def test_unflatten_dict_inverse_with_duplicated_value():
    inv_flat_normal_dict = {v: k for k, v in six.viewitems(flat_normal_dict)}
    inv_flat_normal_dict['2.1.1'] = ('c', 'b', 'a')
    with assert_raises(ValueError):
        unflatten(inv_flat_normal_dict, inverse=True)
