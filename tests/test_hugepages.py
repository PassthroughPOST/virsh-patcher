from xml.etree import ElementTree as ET

import pytest

from virshpatcher.patcher import PatchHugepages
from conftest import assert_nodes, assert_noop

@pytest.fixture
def klass():
    return PatchHugepages


def test_hugepages(patcher, args, tree):
    patcher.patch(tree, args)

    assert_nodes(
        tree,
        './memoryBacking/hugepages',
        {})


def test_noop(patcher, patched_tree, args):
    assert_noop(patcher, patched_tree, args)
