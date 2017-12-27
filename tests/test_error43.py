from xml.etree import ElementTree as ET

import pytest

from virshpatcher.patcher import PatchE43
from conftest import assert_nodes, assert_noop

@pytest.fixture
def klass():
    return PatchE43


def test_kvm_hidden(patcher, args, tree):
    patcher.patch(tree, args)

    assert_nodes(
        tree,
        './features/kvm/hidden',
        {'state': 'on'})


def test_vendor_id(patcher, args, tree):
    patcher.patch(tree, args)

    assert_nodes(
        tree,
        './features/hyperv/vendor_id',
        {'state': 'on',
         'value': patcher.DEFAULT_VENDOR_ID})


def test_set_vendor_id(patcher, args, tree):
    args.vendor_id = 'VENDOR_ID'

    patcher.patch(tree, args)

    assert_nodes(
        tree,
        './features/hyperv/vendor_id',
        {'state': 'on',
         'value': 'VENDOR_ID'})


def test_noop(patcher, patched_tree, args):
    assert_noop(patcher, patched_tree, args)
