#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import argparse
import subprocess
from xml.etree import ElementTree as ET

import libvirt

RUNNING = {
    libvirt.VIR_DOMAIN_RUNNING,
    libvirt.VIR_DOMAIN_PAUSED,
    libvirt.VIR_DOMAIN_PMSUSPENDED,
}

parser = argparse.ArgumentParser(
    add_help=False,
    description='libvirtd xml patcher')

parser.add_argument(
    '--connect', '-c',
    metavar='URI',
    help='hypervisor connection URI',
    default='qemu:///system')

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


def err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def load(module):
    modname, klass = module.rsplit('.', 1)
    x = __import__(modname, fromlist=[klass])
    return getattr(x, klass)


def main():
    args, remainder = parser.parse_known_args()

    patchers = []
    for path in args.patch or []:
        klass = load(path)
        inst = klass(parser)
        patchers.append(inst)

    parser.add_argument(
        'domains',
        metavar='DOMAIN',
        nargs='*')

    args, remainder = parser.parse_known_args(sys.argv[1:])


    if args.help:
        parser.print_help()
        exit(1)

    if not args.domains:
        err("No domains provided.")
        exit(1)

    if not patchers:
        err("No patches provided.")
        exit(1)

    warning = False

    connection = libvirt.open(args.connect)

    for domain in args.domains:

        dom = connection.lookupByName(domain)
        state = dom.info()

        if state[0] in RUNNING:
            warning = True
            err("Warning: Domain '{}' is running. Not applying changes. ".format(
                domain))
            continue

        print("Patching: {}".format(domain))
        tree = ET.fromstring(dom.XMLDesc(0))

        for p in patchers:
            print("> Applying: {}".format(p.__class__.__name__))
            p.patch(tree, args)

        xml_str = ET.tostring(tree).decode()
        connection.defineXML(xml_str)

    if warning:
        exit(1)
