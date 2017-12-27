#!/usr/bin/env python

import os
import sys
import argparse
import importlib
import subprocess
from xml.etree import ElementTree as ET


parser = argparse.ArgumentParser(
    add_help=False,
    description='libvirtd xml patcher')

parser.add_argument(
    '--error43',
    help='Add fixes for \'error43\' with nvidia devices.',
    action='append_const',
    dest='patch',
    const='virshpatcher.patcher.PatchE43')

parser.add_argument(
    '--hugepages',
    help='Make guest use hugepages.',
    action='append_const',
    dest='patch',
    const='virshpatcher.patcher.PatchHugepages')

parser.add_argument(
    '--host-passthrough',
    help='Make guest CPU model `host_passthrough`.',
    action='append_const',
    dest='patch',
    const='virshpatcher.patcher.PatchHostPassthrough')


parser.add_argument(
    '--patch', '-p',
    help='`XMLPatcher` class path',
    action='append',
    dest='patch')

parser.add_argument(
    '--help', '-h',
    help='This help text',
    action='store_true',
    default=False)

def load(module):
    modname, klass = module.rsplit('.', 1)
    x = importlib.__import__(modname, fromlist=[klass])
    return getattr(x, klass)


def main():
    args, remainder = parser.parse_known_args()

    patchers = []
    for path in args.patch:
        klass = load(path)
        inst = klass(parser)
        patchers.append(inst)

    parser.add_argument(
        'file',
        help='XML file to edit, or libvirtd domain.',
        metavar='FILE')

    args = parser.parse_args(sys.argv[1:])
    if args.help:
        parser.print_help()
        exit(1)

    if os.path.exists(args.file):
        tree = ET.parse(args.file)
        for p in patchers:
            p.patch(tree, args)
        tree.write(args.file)

    else:
        os.environ['EDITOR'] = " ".join(sys.argv)
        cmd = ['virsh', 'edit', args.file]
        try:
            ret = subprocess.run(cmd, check=True)
        except Exception as e:
            print("Unable to edit domain {!r}".format(args.file))
            print(e)
            exit(1)
