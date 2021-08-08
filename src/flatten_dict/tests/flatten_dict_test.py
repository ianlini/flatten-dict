from __future__ import absolute_import

import os.path
import json
from types import GeneratorType

import six
import pytest

from flatten_dict import flatten, unflatten
from flatten_dict.reducers import (
    tuple_reducer,
    path_reducer,
    underscore_reducer,
    make_reducer,
)
from flatten_dict.splitters import (
    tuple_splitter,
    path_splitter,
    underscore_splitter,
    make_splitter,
)


@pytest.fixture
def normal_dict():
    return {
        "a": "0",
        "b": {
            "a": "1.0",
            "b": "1.1",
        },
        "c": {
            "a": "2.0",
            "b": {
                "a": "2.1.0",
                "b": "2.1.1",
            },
        },
    }


@pytest.fixture
def flat_tuple_dict():
    return {
        ("a",): "0",
        ("b", "a"): "1.0",
        ("b", "b"): "1.1",
        ("c", "a"): "2.0",
        ("c", "b", "a"): "2.1.0",
        ("c", "b", "b"): "2.1.1",
    }


@pytest.fixture
def flat_tuple_dict_depth2():
    return {
        ("a",): "0",
        ("b", "a"): "1.0",
        ("b", "b"): "1.1",
        ("c", "a"): "2.0",
        ("c", "b"): {"a": "2.1.0", "b": "2.1.1"},
    }


def get_flat_tuple_dict(flat_tuple_dict):
    return flat_tuple_dict


def get_flat_path_dict(flat_tuple_dict):
    return {os.path.join(*k): v for k, v in six.viewitems(flat_tuple_dict)}


def get_flat_underscore_dict(flat_tuple_dict):
    return {"_".join(k): v for k, v in six.viewitems(flat_tuple_dict)}


@pytest.fixture
def inv_flat_tuple_dict(flat_tuple_dict):
    return {v: k for k, v in six.viewitems(flat_tuple_dict)}


def test_flatten_dict(normal_dict, flat_tuple_dict):
    assert flatten(normal_dict) == flat_tuple_dict


def test_flatten_dict_invalid_depth_limit(normal_dict):
    with pytest.raises(ValueError):
        flatten(normal_dict, max_flatten_depth=0)


def test_flatten_dict_depth_limit_1(normal_dict):
    flattened = flatten(normal_dict, max_flatten_depth=1)
    values_before = sorted(
        flattened.values(), key=lambda x: json.dumps(x, sort_keys=True)
    )
    values_after = sorted(
        normal_dict.values(), key=lambda x: json.dumps(x, sort_keys=True)
    )
    assert values_before == values_after


def test_flatten_dict_depth_limit_2(normal_dict, flat_tuple_dict_depth2):
    assert flatten(normal_dict, max_flatten_depth=2) == flat_tuple_dict_depth2


def test_flatten_dict_irrelevant_depth_limit(normal_dict, flat_tuple_dict):
    assert flatten(normal_dict, max_flatten_depth=3) == flat_tuple_dict


def test_flatten_nonflattenable_type():
    with pytest.raises(ValueError):
        flatten([])


@pytest.mark.parametrize(
    "reducer, expected_flat_dict_func",
    [
        ("tuple", get_flat_tuple_dict),
        ("path", get_flat_path_dict),
        ("underscore", get_flat_underscore_dict),
        (tuple_reducer, get_flat_tuple_dict),
        (path_reducer, get_flat_path_dict),
        (underscore_reducer, get_flat_underscore_dict),
    ],
)
def test_flatten_dict_with_reducer(
    normal_dict, flat_tuple_dict, reducer, expected_flat_dict_func
):
    expected_flat_dict = expected_flat_dict_func(flat_tuple_dict)
    assert flatten(normal_dict, reducer=reducer) == expected_flat_dict


def test_flatten_dict_inverse(normal_dict, inv_flat_tuple_dict):
    assert flatten(normal_dict, inverse=True) == inv_flat_tuple_dict


def test_flatten_dict_inverse_with_duplicated_value(normal_dict):
    dup_val_dict = normal_dict.copy()
    dup_val_dict["a"] = "2.1.1"
    with pytest.raises(ValueError):
        flatten(dup_val_dict, inverse=True)


def test_unflatten_dict(normal_dict, flat_tuple_dict):
    assert unflatten(flat_tuple_dict) == normal_dict


def test_unflatten_dict_inverse(normal_dict, inv_flat_tuple_dict):
    assert unflatten(inv_flat_tuple_dict, inverse=True) == normal_dict


@pytest.mark.parametrize(
    "splitter, flat_dict_func",
    [
        ("tuple", get_flat_tuple_dict),
        ("path", get_flat_path_dict),
        ("underscore", get_flat_underscore_dict),
        (tuple_splitter, get_flat_tuple_dict),
        (path_splitter, get_flat_path_dict),
        (underscore_splitter, get_flat_underscore_dict),
    ],
)
def test_unflatten_dict_with_splitter(
    normal_dict, flat_tuple_dict, splitter, flat_dict_func
):
    flat_dict = flat_dict_func(flat_tuple_dict)
    assert unflatten(flat_dict, splitter=splitter) == normal_dict


def test_unflatten_dict_inverse_with_duplicated_value(
    flat_tuple_dict, inv_flat_tuple_dict
):
    inv_flat_tuple_dict["2.1.1"] = ("c", "b", "a")
    with pytest.raises(ValueError):
        unflatten(inv_flat_tuple_dict, inverse=True)


@pytest.fixture
def dict_with_list():
    return {
        "a": "0",
        "b": {
            "a": "1.0",
            "b": "1.1",
        },
        "c": {
            "a": "2.0",
            "b": {
                "a": "2.1.0",
                "b": ["2.1.1.0", "2.1.1.1"],
                "c": [],
            },
        },
    }


@pytest.fixture
def flat_tuple_dict_with_list():
    return {
        ("a",): "0",
        ("b", "a"): "1.0",
        ("b", "b"): "1.1",
        ("c", "a"): "2.0",
        ("c", "b", "a"): "2.1.0",
        ("c", "b", "b"): ["2.1.1.0", "2.1.1.1"],
        ("c", "b", "c"): [],
    }


@pytest.fixture
def flat_tuple_dict_with_list_depth2():
    return {
        ("a",): "0",
        ("b", "a"): "1.0",
        ("b", "b"): "1.1",
        ("c", "a"): "2.0",
        ("c", "b"): {
            "a": "2.1.0",
            "b": ["2.1.1.0", "2.1.1.1"],
            "c": [],
        },
    }


def test_flatten_dict_with_list(dict_with_list, flat_tuple_dict_with_list):
    assert flatten(dict_with_list) == flat_tuple_dict_with_list


def test_flatten_dict_with_list_depth_limit_1(dict_with_list):
    flattened = flatten(dict_with_list, max_flatten_depth=1)
    before = sorted(dict_with_list.items(), key=lambda x: x[0])
    after = sorted(flattened.items(), key=lambda x: x[0])
    # flatten with the default reducer transforms keys to tuples
    after = [(x[0][0], x[1]) for x in after]
    assert before == after


def test_flatten_dict_with_list_depth_limit_2(
    dict_with_list, flat_tuple_dict_with_list_depth2
):
    assert (
        flatten(dict_with_list, max_flatten_depth=2) == flat_tuple_dict_with_list_depth2
    )


def test_flatten_dict_with_list_irrelevant_depth_limit(
    dict_with_list, flat_tuple_dict_with_list
):
    assert flatten(dict_with_list, max_flatten_depth=3) == flat_tuple_dict_with_list


@pytest.mark.parametrize(
    "reducer, expected_flat_dict_func",
    [
        ("tuple", get_flat_tuple_dict),
        ("path", get_flat_path_dict),
        ("underscore", get_flat_underscore_dict),
        (tuple_reducer, get_flat_tuple_dict),
        (path_reducer, get_flat_path_dict),
        (underscore_reducer, get_flat_underscore_dict),
    ],
)
def test_flatten_dict_with_list_with_reducer(
    dict_with_list, flat_tuple_dict_with_list, reducer, expected_flat_dict_func
):
    expected_flat_dict = expected_flat_dict_func(flat_tuple_dict_with_list)
    assert flatten(dict_with_list, reducer=reducer) == expected_flat_dict


def test_unflatten_dict_with_list(dict_with_list, flat_tuple_dict_with_list):
    assert unflatten(flat_tuple_dict_with_list) == dict_with_list


@pytest.mark.parametrize(
    "splitter, flat_dict_func",
    [
        ("tuple", get_flat_tuple_dict),
        ("path", get_flat_path_dict),
        ("underscore", get_flat_underscore_dict),
        (tuple_splitter, get_flat_tuple_dict),
        (path_splitter, get_flat_path_dict),
        (underscore_splitter, get_flat_underscore_dict),
    ],
)
def test_unflatten_dict_with_list_with_splitter(
    dict_with_list, flat_tuple_dict_with_list, splitter, flat_dict_func
):
    flat_dict = flat_dict_func(flat_tuple_dict_with_list)
    assert unflatten(flat_dict, splitter=splitter) == dict_with_list


@pytest.fixture
def flat_tuple_dict_with_enumerated_list():
    return {
        ("a",): "0",
        ("b", "a"): "1.0",
        ("b", "b"): "1.1",
        ("c", "a"): "2.0",
        ("c", "b", "a"): "2.1.0",
        ("c", "b", "b", 0): "2.1.1.0",
        ("c", "b", "b", 1): "2.1.1.1",
    }


def test_flatten_dict_with_list_with_enumerate_types(
    dict_with_list, flat_tuple_dict_with_enumerated_list
):
    assert (
        flatten(dict_with_list, enumerate_types=(list,))
        == flat_tuple_dict_with_enumerated_list
    )


def test_flatten_list():
    assert flatten([1, 2], enumerate_types=(list,)) == {(0,): 1, (1,): 2}


@pytest.fixture
def dict_with_generator():
    return {
        "a": "0",
        "b": {
            "a": "1.0",
            "b": "1.1",
        },
        "c": {
            "a": "2.0",
            "b": {
                "a": "2.1.0",
                "b": ("2.1.1.%d" % i for i in range(2)),
                "c": (i for i in ()),  # empty generator
            },
        },
    }


def test_flatten_dict_with_generator_with_enumerate_types(
    dict_with_generator, flat_tuple_dict_with_enumerated_list
):
    assert (
        flatten(dict_with_generator, enumerate_types=(GeneratorType,))
        == flat_tuple_dict_with_enumerated_list
    )


@pytest.fixture
def dict_with_empty_dict():
    return {
        "a": "0",
        "b": {
            "a": "1.0",
            "b": "1.1",
        },
        "c": {
            "a": "2.0",
            "b": {
                "a": "2.1.0",
                "b": "2.1.1",
                "c": {},
            },
        },
    }


@pytest.fixture
def flat_tuple_dict_with_empty_dict():
    return {
        ("a",): "0",
        ("b", "a"): "1.0",
        ("b", "b"): "1.1",
        ("c", "a"): "2.0",
        ("c", "b", "a"): "2.1.0",
        ("c", "b", "b"): "2.1.1",
        ("c", "b", "c"): {},
    }


def test_flatten_dict_with_empty_dict(dict_with_empty_dict, flat_tuple_dict):
    assert flatten(dict_with_empty_dict) == flat_tuple_dict


def test_flatten_dict_with_empty_dict_kept(
    dict_with_empty_dict, flat_tuple_dict_with_empty_dict
):
    assert (
        flatten(dict_with_empty_dict, keep_empty_types=(dict,))
        == flat_tuple_dict_with_empty_dict
    )


def test_flatten_dict_with_keep_empty_types(normal_dict, flat_tuple_dict):
    assert flatten(normal_dict, keep_empty_types=(dict, str)) == flat_tuple_dict


@pytest.mark.parametrize(
    "delimiter, delimiter_equivalent", [(".", "dot"), ("_", "underscore")]
)
def test_make_reducer(normal_dict, delimiter, delimiter_equivalent):
    reducer = make_reducer(delimiter)
    flattened_dict_using_make_reducer = flatten(normal_dict, reducer=reducer)
    flattened_dict_using_equivalent_reducer = flatten(
        normal_dict, reducer=delimiter_equivalent
    )
    assert flattened_dict_using_make_reducer == flattened_dict_using_equivalent_reducer


@pytest.mark.parametrize(
    "delimiter, delimiter_equivalent", [(".", "dot"), ("_", "underscore")]
)
def test_make_splitter(normal_dict, delimiter, delimiter_equivalent):
    splitter = make_splitter(delimiter)
    flat_dict = flatten(normal_dict, delimiter_equivalent)
    unflattened_dict_using_make_splitter = unflatten(flat_dict, splitter=splitter)
    unflattened_dict_using_equivalent_splitter = unflatten(
        flat_dict, splitter=delimiter_equivalent
    )
    assert (
        unflattened_dict_using_make_splitter
        == unflattened_dict_using_equivalent_splitter
    )
