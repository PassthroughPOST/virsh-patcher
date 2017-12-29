Virsh Patcher ![](https://travis-ci.org/PassthroughPOST/virsh-patcher.svg?branch=master)
===================

Simple utility to apply common changes to libvirtd guests.

Changes will not be applied if the guest is running.


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
usage: virshpatcher [--connect URI] [--error43] [--hugepages]
                    [--host-passthrough] [--patch PATCH] [--help]
                    [--vendor-id ab1234567890] [--random-vendor-id]
                    [DOMAIN [DOMAIN ...]]

libvirtd xml patcher

positional arguments:
  DOMAIN

optional arguments:
  --connect URI, -c URI
                        hypervisor connection URI
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

 * Add ability to connect PCI devices to guest (By name/pattern/id?)
 * Interactive (?)
 * More tests.
