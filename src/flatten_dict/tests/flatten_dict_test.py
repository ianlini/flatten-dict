from __future__ import absolute_import

import os.path
import json
from types import GeneratorType
import sys
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

import pytest

from flatten_dict import flatten, unflatten, TReducerCallable
from flatten_dict.flatten_dict import TKeyIn
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

TNormalDict = Dict[str, Union[str, Dict[str, Union[str, Dict[str, str]]]]]


@pytest.fixture
def normal_dict() -> TNormalDict:
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


TFlatTupleDict = Dict[Tuple[str, ...], str]


@pytest.fixture
def flat_tuple_dict() -> TFlatTupleDict:
    return {
        ("a",): "0",
        ("b", "a"): "1.0",
        ("b", "b"): "1.1",
        ("c", "a"): "2.0",
        ("c", "b", "a"): "2.1.0",
        ("c", "b", "b"): "2.1.1",
    }


TFlatTupleDictDepth2 = Dict[Tuple[str, ...], Union[str, Dict[str, str]]]


@pytest.fixture
def flat_tuple_dict_depth2() -> TFlatTupleDictDepth2:
    return {
        ("a",): "0",
        ("b", "a"): "1.0",
        ("b", "b"): "1.1",
        ("c", "a"): "2.0",
        ("c", "b"): {"a": "2.1.0", "b": "2.1.1"},
    }


TNormalDictWithNestedLists = Dict[
    str,
    Union[
        str,
        List[Union[str, Dict[str, str], List[str], Dict[str, List[str]]]],
    ],
]


@pytest.fixture
def normal_dict_with_nested_lists() -> TNormalDictWithNestedLists:
    return {
        "aaa": "0",
        "bbb": ["1.1", "1.2", "1.3"],
        "ccc": [{"aaa": "2.1.1"}, {"aaa": "2.2.1"}],
        "ddd": [["3.1.1", "3.1.2", "3.1.3"], ["3.2.1", "3.2.2", "3.2.3"]],
        "eee": [
            {"aaa": ["4.1.1", "4.1.2", "4.1.3"]},
            {"bbb": ["4.2.1", "4.2.2", "4.2.3"]},
        ],
    }


@pytest.fixture
def flat_dict_with_nested_lists_with_list_syntax() -> Dict[str, str]:
    return {
        "aaa": "0",
        "bbb[0]": "1.1",
        "bbb[1]": "1.2",
        "bbb[2]": "1.3",
        "ccc[0].aaa": "2.1.1",
        "ccc[1].aaa": "2.2.1",
        "ddd[0][0]": "3.1.1",
        "ddd[0][1]": "3.1.2",
        "ddd[0][2]": "3.1.3",
        "ddd[1][0]": "3.2.1",
        "ddd[1][1]": "3.2.2",
        "ddd[1][2]": "3.2.3",
        "eee[0].aaa[0]": "4.1.1",
        "eee[0].aaa[1]": "4.1.2",
        "eee[0].aaa[2]": "4.1.3",
        "eee[1].bbb[0]": "4.2.1",
        "eee[1].bbb[1]": "4.2.2",
        "eee[1].bbb[2]": "4.2.3",
    }


T = TypeVar("T")


def get_flat_tuple_dict(flat_tuple_dict: T) -> T:
    return flat_tuple_dict


def get_flat_path_dict(flat_tuple_dict: TFlatTupleDict) -> Dict[str, str]:
    return {os.path.join(*k): v for k, v in flat_tuple_dict.items()}


def get_flat_underscore_dict(flat_tuple_dict: TFlatTupleDict) -> Dict[str, str]:
    return {"_".join(k): v for k, v in flat_tuple_dict.items()}


TInvFlatTupleDict = Dict[str, Tuple[str, ...]]


@pytest.fixture
def inv_flat_tuple_dict(flat_tuple_dict: TFlatTupleDict) -> TInvFlatTupleDict:
    return {v: k for k, v in flat_tuple_dict.items()}


def test_flatten_dict(
    normal_dict: TNormalDict, flat_tuple_dict: TFlatTupleDict
) -> None:
    assert flatten(normal_dict) == flat_tuple_dict


def test_flatten_dict_invalid_depth_limit(normal_dict: TNormalDict) -> None:
    with pytest.raises(ValueError):
        flatten(normal_dict, max_flatten_depth=0)


def test_flatten_dict_depth_limit_1(normal_dict: TNormalDict) -> None:
    flattened = flatten(normal_dict, max_flatten_depth=1)
    values_before = sorted(
        flattened.values(), key=lambda x: json.dumps(x, sort_keys=True)
    )
    values_after = sorted(
        normal_dict.values(), key=lambda x: json.dumps(x, sort_keys=True)
    )
    assert values_before == values_after


def test_flatten_dict_depth_limit_2(
    normal_dict: TNormalDict, flat_tuple_dict_depth2: TFlatTupleDictDepth2
) -> None:
    assert flatten(normal_dict, max_flatten_depth=2) == flat_tuple_dict_depth2


def test_flatten_dict_irrelevant_depth_limit(
    normal_dict: TNormalDict, flat_tuple_dict: TFlatTupleDict
) -> None:
    assert flatten(normal_dict, max_flatten_depth=3) == flat_tuple_dict


def test_flatten_nonflattenable_type() -> None:
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
    normal_dict: TNormalDict,
    flat_tuple_dict: TFlatTupleDict,
    reducer: TReducerCallable,
    expected_flat_dict_func: Callable[
        [TFlatTupleDict], Union[TFlatTupleDict, Dict[str, str]]
    ],
) -> None:
    expected_flat_dict = expected_flat_dict_func(flat_tuple_dict)
    assert flatten(normal_dict, reducer=reducer) == expected_flat_dict


def test_flatten_dict_inverse(
    normal_dict: TNormalDict, inv_flat_tuple_dict: TInvFlatTupleDict
) -> None:
    assert flatten(normal_dict, inverse=True) == inv_flat_tuple_dict


def test_flatten_dict_inverse_with_duplicated_value(normal_dict: TNormalDict) -> None:
    dup_val_dict = normal_dict.copy()
    dup_val_dict["a"] = "2.1.1"
    with pytest.raises(ValueError):
        flatten(dup_val_dict, inverse=True)


def test_flatten_dict_with_list_syntax(
    normal_dict_with_nested_lists: TNormalDictWithNestedLists,
    flat_dict_with_nested_lists_with_list_syntax: Dict[str, str],
) -> None:
    def _reducer(
        parent_path: Optional[Union[str, int]],
        key: Union[str, int],
        parent_obj: Union[Iterable[Any], Mapping[str, Any]],
    ) -> Union[str, int]:
        if parent_path is None:
            return key
        elif isinstance(parent_obj, list):
            return "{}[{}]".format(parent_path, key)
        else:
            return "{}.{}".format(parent_path, key)

    assert (
        flatten(
            normal_dict_with_nested_lists, reducer=_reducer, enumerate_types=(list,)
        )
        == flat_dict_with_nested_lists_with_list_syntax
    )


def test_unflatten_dict(
    normal_dict: TNormalDict, flat_tuple_dict: TFlatTupleDict
) -> None:
    assert unflatten(flat_tuple_dict) == normal_dict


def test_unflatten_dict_inverse(
    normal_dict: TNormalDict, inv_flat_tuple_dict: TInvFlatTupleDict
) -> None:
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
    normal_dict: TNormalDict,
    flat_tuple_dict: TFlatTupleDict,
    splitter: Callable[[str], Tuple[Any, ...]],
    flat_dict_func: Callable[[TFlatTupleDict], Dict[str, str]],
) -> None:
    flat_dict = flat_dict_func(flat_tuple_dict)
    assert unflatten(flat_dict, splitter=splitter) == normal_dict


def test_unflatten_dict_inverse_with_duplicated_value(
    inv_flat_tuple_dict: TInvFlatTupleDict,
) -> None:
    inv_flat_tuple_dict["2.1.1"] = ("c", "b", "a")
    with pytest.raises(ValueError):
        unflatten(inv_flat_tuple_dict, inverse=True)


TDictWithLists = Dict[
    str, Union[str, Dict[str, Union[str, Dict[str, Union[str, Sequence[str]]]]]]
]


@pytest.fixture
def dict_with_list() -> TDictWithLists:
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


TFlatTupleDictWithList = Dict[Tuple[str, ...], Union[str, Sequence[str]]]


@pytest.fixture
def flat_tuple_dict_with_list() -> TFlatTupleDictWithList:
    return {
        ("a",): "0",
        ("b", "a"): "1.0",
        ("b", "b"): "1.1",
        ("c", "a"): "2.0",
        ("c", "b", "a"): "2.1.0",
        ("c", "b", "b"): ["2.1.1.0", "2.1.1.1"],
        ("c", "b", "c"): [],
    }


TFlatTupleDictWithListDepth2 = Dict[
    Tuple[str, ...], Union[str, Dict[str, Union[str, Sequence[str]]]]
]


@pytest.fixture
def flat_tuple_dict_with_list_depth2() -> TFlatTupleDictWithListDepth2:
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


def test_flatten_dict_with_list(
    dict_with_list: TDictWithLists, flat_tuple_dict_with_list: TFlatTupleDictWithList
) -> None:
    assert flatten(dict_with_list) == flat_tuple_dict_with_list


def test_flatten_dict_with_list_depth_limit_1(dict_with_list: TDictWithLists) -> None:
    # TODO: type of key should be possible to infer
    flattened: Dict[Tuple[str, ...], str] = flatten(dict_with_list, max_flatten_depth=1)
    before = sorted(dict_with_list.items(), key=lambda x: x[0])
    _after = sorted(flattened.items(), key=lambda x: x[0])
    # flatten with the default reducer transforms keys to tuples
    after = [(key, val) for (key,), val in _after]
    assert before == after


def test_flatten_dict_with_list_depth_limit_2(
    dict_with_list: TDictWithLists,
    flat_tuple_dict_with_list_depth2: TFlatTupleDictWithListDepth2,
) -> None:
    assert (
        flatten(dict_with_list, max_flatten_depth=2) == flat_tuple_dict_with_list_depth2
    )


def test_flatten_dict_with_list_irrelevant_depth_limit(
    dict_with_list: TDictWithLists, flat_tuple_dict_with_list: TFlatTupleDictWithList
) -> None:
    assert flatten(dict_with_list, max_flatten_depth=3) == flat_tuple_dict_with_list


TFlatDictCallable = Callable[
    [TFlatTupleDictWithList], Union[TDictWithLists, TFlatTupleDictWithList]
]


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
    dict_with_list: TDictWithLists,
    flat_tuple_dict_with_list: TFlatTupleDictWithList,
    reducer: TReducerCallable,
    expected_flat_dict_func: TFlatDictCallable,
) -> None:
    expected_flat_dict = expected_flat_dict_func(flat_tuple_dict_with_list)
    assert flatten(dict_with_list, reducer=reducer) == expected_flat_dict


def test_unflatten_dict_with_list(
    dict_with_list: TDictWithLists, flat_tuple_dict_with_list: TFlatTupleDictWithList
) -> None:
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
    dict_with_list: TDictWithLists,
    flat_tuple_dict_with_list: TFlatTupleDictWithList,
    splitter: Callable[[TKeyIn], Tuple[str, ...]],
    flat_dict_func: Callable[
        [TFlatTupleDictWithList],
        Dict[TKeyIn, Union[str, List[str]]],
    ],
) -> None:
    flat_dict = flat_dict_func(flat_tuple_dict_with_list)
    assert unflatten(flat_dict, splitter=splitter) == dict_with_list


TFlatTupleDictWithEnumeratedList = Dict[Tuple[Union[str, int], ...], str]


@pytest.fixture
def flat_tuple_dict_with_enumerated_list() -> TFlatTupleDictWithEnumeratedList:
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
    dict_with_list: TDictWithLists,
    flat_tuple_dict_with_enumerated_list: TFlatTupleDictWithEnumeratedList,
) -> None:
    assert (
        flatten(dict_with_list, enumerate_types=(list,))
        == flat_tuple_dict_with_enumerated_list
    )


def test_flatten_list() -> None:
    assert flatten([1, 2], enumerate_types=(list,)) == {(0,): 1, (1,): 2}


TDictWithGenerator = Dict[
    str, Union[str, Dict[str, Union[str, Dict[str, Union[str, Iterator[str]]]]]]
]


@pytest.fixture
def dict_with_generator() -> TDictWithGenerator:
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
                "c": (i for i in ""),  # empty generator
            },
        },
    }


def test_flatten_dict_with_generator_with_enumerate_types(
    dict_with_generator: TDictWithGenerator,
    flat_tuple_dict_with_enumerated_list: TFlatTupleDictWithEnumeratedList,
) -> None:
    assert (
        flatten(dict_with_generator, enumerate_types=(GeneratorType,))
        == flat_tuple_dict_with_enumerated_list
    )


TDictWithEmptyDict = Dict[
    str, Union[str, Dict[str, Union[str, Dict[str, Union[str, Dict]]]]]
]


@pytest.fixture
def dict_with_empty_dict() -> TDictWithEmptyDict:
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


TFlatTupleDictWithEmptyDict = Dict[Tuple[str, ...], Union[str, Dict]]


@pytest.fixture
def flat_tuple_dict_with_empty_dict() -> TFlatTupleDictWithEmptyDict:
    return {
        ("a",): "0",
        ("b", "a"): "1.0",
        ("b", "b"): "1.1",
        ("c", "a"): "2.0",
        ("c", "b", "a"): "2.1.0",
        ("c", "b", "b"): "2.1.1",
        ("c", "b", "c"): {},
    }


def test_flatten_dict_with_empty_dict(
    dict_with_empty_dict: TDictWithEmptyDict,
    flat_tuple_dict: TFlatTupleDictWithEmptyDict,
) -> None:
    assert flatten(dict_with_empty_dict) == flat_tuple_dict


def test_flatten_dict_with_empty_dict_kept(
    dict_with_empty_dict: TDictWithEmptyDict,
    flat_tuple_dict_with_empty_dict: TFlatTupleDictWithEmptyDict,
) -> None:
    assert (
        flatten(dict_with_empty_dict, keep_empty_types=(dict,))
        == flat_tuple_dict_with_empty_dict
    )


def test_flatten_dict_with_keep_empty_types(
    normal_dict: TNormalDict, flat_tuple_dict: TFlatTupleDict
) -> None:
    assert flatten(normal_dict, keep_empty_types=(dict, str)) == flat_tuple_dict


@pytest.mark.parametrize(
    "delimiter, delimiter_equivalent", [(".", "dot"), ("_", "underscore")]
)
def test_make_reducer(
    normal_dict: TNormalDict,
    delimiter: str,
    delimiter_equivalent: Literal["dot", "underscore"],
) -> None:
    # use explicit type to narrow default reducer
    reducer: Callable[
        [Union[str, int, None], Union[str, int]], Union[str, int]
    ] = make_reducer(delimiter)
    flattened_dict_using_make_reducer = flatten(normal_dict, reducer=reducer)
    flattened_dict_using_equivalent_reducer = flatten(
        normal_dict, reducer=delimiter_equivalent
    )
    assert flattened_dict_using_make_reducer == flattened_dict_using_equivalent_reducer


@pytest.mark.parametrize(
    "delimiter, delimiter_equivalent", [(".", "dot"), ("_", "underscore")]
)
def test_make_splitter(
    normal_dict: TNormalDict,
    delimiter: str,
    delimiter_equivalent: Literal["dot", "underscore"],
) -> None:
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
