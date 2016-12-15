import six

from flatten_dict import flatten


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
