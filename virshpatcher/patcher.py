import random
from xml.etree import ElementTree as ET


class XMLPatcher(object):

    def __init__(self, parser):
        self.add_arguments(parser)

    def add_arguments(self, parser):
        pass

    def patch(self, tree, args):
        node = tree.getroot()

        for tag in self.nodes:
            creator = getattr(
                self,
                'create_' + tag,
                lambda args: (tag, {}))

            patcher = getattr(
                self,
                'patch_' + tag,
                lambda args, node: node)

            new = node.find(tag)

            if new is None:
                new = ET.SubElement(node, *creator(args))

            patcher(args, new)
            node = new


class PatchE43(XMLPatcher):
    DEFAULT_VENDOR_ID = 'ab1234567890'

    nodes = ['features', 'hyperv', 'vendor_id']

    def add_arguments(self, parser):
        parser.add_argument(
            '--vendor-id',
            help='Vendor ID for E43 patch.',
            metavar=self.DEFAULT_VENDOR_ID,
            default=self.DEFAULT_VENDOR_ID)
        parser.add_argument(
            '--random-vendor-id',
            help='Set a random Vendor ID.',
            action='store_true',
            default=False)

    def patch_vendor_id(self, args, node):
        node.set('state', 'on')

        if args.random_vendor_id:
            vendor_id = "".join([
                random.choice('1234567890abcdef')
                for _ in range(12)])
        else:
            vendor_id = args.vendor_id

        node.set('value', vendor_id)


class PatchHugepages(XMLPatcher):
    nodes = ['memoryBacking', 'hugepages']


class PatchHostPassthrough(XMLPatcher):
    nodes = ['cpu']

    def patch_cpu(self, args, node):
        node.clear()
        node.set('mode', 'host-passthrough')
        node.set('check', 'partial')
