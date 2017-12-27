import os
import argparse
from xml.etree import ElementTree as ET

import pytest


@pytest.fixture
def args_list():
    return []

@pytest.fixture
def args(parser, args_list):
    return parser.parse_args(args_list)


@pytest.fixture
def parser():
    return argparse.ArgumentParser()


@pytest.fixture
def tree():
    root = os.path.dirname(__file__)
    return ET.parse(os.path.join(root, 'test.xml'))


@pytest.fixture
def patched_tree():
    root = os.path.dirname(__file__)
    return ET.parse(os.path.join(root, 'patched.xml'))


@pytest.fixture
def patcher(klass, parser):
    return klass(parser)


def assert_nodes(tree, xpath, attributes):
    nodes = tree.findall(xpath)
    assert len(nodes) == 1
    assert nodes[0].attrib == attributes


def assert_noop(patcher, tree, args):
    original = ET.tostring(tree.getroot())

    patcher.patch(tree, args)

    patched = ET.tostring(tree.getroot())

    assert patched == original
