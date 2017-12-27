Virsh Patcher
==================

Simple utility to apply common changes to libvirtd domain xml files.

Can either edit the xml file directly, or apply the patch via a hack around `virsh edit`.


Supported Fixes
-------------------

 * Error 43 for Nvidia GPUs
 * Hugepages memory backing
 * `host-passthrough` CPU type.

Installation
---------------

```
$ pip install https://github.com/xlevus/virsh-patcher/archive/master.zip
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
