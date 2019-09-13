from __future__ import absolute_import
import os.path

import six
import pytest

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


def test_flatten_nonflattenable_type():
    with pytest.raises(ValueError):
        flatten([])


def test_flatten_dict_inverse():
    inv_flat_normal_dict = {v: k for k, v in six.viewitems(flat_normal_dict)}
    assert flatten(normal_dict, inverse=True) == inv_flat_normal_dict


def test_flatten_dict_with_reducer():
    assert flatten(normal_dict, reducer=tuple_reducer) == flat_normal_dict


def test_flatten_dict_path():
    flat_path_dict = {os.path.join(*k): v for k, v in six.viewitems(flat_normal_dict)}
    assert flatten(normal_dict, reducer='path') == flat_path_dict


def test_flatten_dict_underscore():
    flat_underscore_dict = {'_'.join(k): v for k, v in six.viewitems(flat_normal_dict)}
    assert flatten(normal_dict, reducer='underscore') == flat_underscore_dict


def test_flatten_dict_inverse_with_duplicated_value():
    dup_val_dict = normal_dict.copy()
    dup_val_dict['a'] = '2.1.1'
    with pytest.raises(ValueError):
        flatten(dup_val_dict, inverse=True)


def test_unflatten_dict():
    assert unflatten(flat_normal_dict) == normal_dict


def test_unflatten_dict_inverse():
    inv_flat_normal_dict = {v: k for k, v in six.viewitems(flat_normal_dict)}
    assert unflatten(inv_flat_normal_dict, inverse=True) == normal_dict


def test_unflatten_dict_with_splitter():
    assert unflatten(flat_normal_dict, splitter=tuple_splitter) == normal_dict


def test_unflatten_dict_path():
    flat_path_dict = {os.path.join(*k): v for k, v in six.viewitems(flat_normal_dict)}
    assert unflatten(flat_path_dict, splitter='path') == normal_dict


def test_unflatten_dict_underscore():
    flat_underscore_dict = {'_'.join(k): v for k, v in six.viewitems(flat_normal_dict)}
    assert unflatten(flat_underscore_dict, splitter='underscore') == normal_dict


def test_unflatten_dict_inverse_with_duplicated_value():
    inv_flat_normal_dict = {v: k for k, v in six.viewitems(flat_normal_dict)}
    inv_flat_normal_dict['2.1.1'] = ('c', 'b', 'a')
    with pytest.raises(ValueError):
        unflatten(inv_flat_normal_dict, inverse=True)


dict_with_list = {
    'a': '0',
    'b': {
        'a': '1.0',
        'b': '1.1',
    },
    'c': {
        'a': '2.0',
        'b': {
            'a': '2.1.0',
            'b': ['2.1.1.0', '2.1.1.1'],
        },
    },
}


flat_dict_with_list = {
    ('a',): '0',
    ('b', 'a'): '1.0',
    ('b', 'b'): '1.1',
    ('c', 'a'): '2.0',
    ('c', 'b', 'a'): '2.1.0',
    ('c', 'b', 'b'): ['2.1.1.0', '2.1.1.1'],
}


def test_flatten_dict_with_list():
    assert flatten(dict_with_list) == flat_dict_with_list


def test_flatten_dict_with_list_with_reducer():
    assert flatten(dict_with_list, reducer=tuple_reducer) == flat_dict_with_list


def test_flatten_dict_with_list_path():
    flat_path_dict = {os.path.join(*k): v for k, v in six.viewitems(flat_dict_with_list)}
    assert flatten(dict_with_list, reducer='path') == flat_path_dict


def test_flatten_dict_with_list_underscore():
    flat_underscore_dict = {'_'.join(k): v for k, v in six.viewitems(flat_dict_with_list)}
    assert flatten(dict_with_list, reducer='underscore') == flat_underscore_dict


def test_unflatten_dict_with_list():
    assert unflatten(flat_dict_with_list) == dict_with_list


def test_unflatten_dict_with_list_with_splitter():
    assert unflatten(flat_dict_with_list, splitter=tuple_splitter) == dict_with_list


def test_unflatten_dict_with_list_path():
    flat_path_dict = {os.path.join(*k): v for k, v in six.viewitems(flat_dict_with_list)}
    assert unflatten(flat_path_dict, splitter='path') == dict_with_list


def test_unflatten_dict_with_list_underscore():
    flat_underscore_dict = {'_'.join(k): v for k, v in six.viewitems(flat_dict_with_list)}
    assert unflatten(flat_underscore_dict, splitter='underscore') == dict_with_list


flat_dict_with_enumerated_list = {
    ('a',): '0',
    ('b', 'a'): '1.0',
    ('b', 'b'): '1.1',
    ('c', 'a'): '2.0',
    ('c', 'b', 'a'): '2.1.0',
    ('c', 'b', 'b', 0): '2.1.1.0',
    ('c', 'b', 'b', 1): '2.1.1.1',
}


def test_flatten_dict_with_list_with_enumerate_types():
    assert flatten(dict_with_list, enumerate_types=(list,)) == flat_dict_with_enumerated_list


def test_flatten_list():
    assert flatten([1, 2], enumerate_types=(list,)) == {(0,): 1, (1,): 2}
