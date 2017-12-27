from xml.etree import ElementTree as ET

import pytest

from virshpatcher.patcher import PatchHostPassthrough
from conftest import assert_nodes, assert_noop

@pytest.fixture
def klass():
    return PatchHostPassthrough


def test_hugepages(patcher, args, tree):
    patcher.patch(tree, args)

    assert_nodes(
        tree,
        './cpu',
        {'check': 'partial',
         'mode': 'host-passthrough'})


def test_noop(patcher, patched_tree, args):
    assert_noop(patcher, patched_tree, args)
