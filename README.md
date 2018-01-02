Virsh Patcher ![](https://travis-ci.org/PassthroughPOST/virsh-patcher.svg?branch=master)
===================

Simple utility to apply common changes to libvirtd domain xml files.

Can either edit the xml file directly, or apply the patch via a hack around `virsh edit`.


Supported Fixes
-------------------

 * Error 43 for Nvidia GPUs
 * Hugepages memory backing
 * `host-passthrough` CPU type.

Installation
---------------

### Arch Linux
Install [virshpatcher](https://aur.archlinux.org/packages/virshpatcher/) from the AUR.

### Others
Use `pip`:

```
$ pip install -U https://github.com/PassthroughPOST/virsh-patcher/archive/master.zip
```


Usage
------

```
$ virshpatcher --error43 --hugepages --host-passthrough win10-guest
```

```
$ virshpatcher --help
usage: virshpatcher [--error43] [--hugepages] [--host-passthrough]
                    [--patch PATCH] [--help]
                    [FILE]

libvirtd xml patcher

positional arguments:
  FILE                  XML file to edit, or libvirtd domain.

optional arguments:
  --error43             Add fixes for 'error43' with nvidia devices.
  --hugepages           Make guest use hugepages.
  --host-passthrough    Make guest CPU model `host_passthrough`.
  --patch PATCH, -p PATCH
                        `XMLPatcher` class path
  --help, -h            This help text
  --vendor-id ab1234567890
                        Vendor ID for E43 patch.
  --random-vendor-id    Set a random Vendor ID.

```

Future Improvements
-----------------------

 * Use libvirt API instead of `virsh edit` hack.
 * Add ability to connect PCI devices to guest (By name/pattern/id?)
 * Interactive (?)
 * More tests.
