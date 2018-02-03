#!/usr/bin/env python

from setuptools import setup


setup(
    name='virshpatcher',
    version='1.0.0a1',
    description='Utility to apply common patches to virsh xml files.',
    packages=['virshpatcher'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=[],
    install_requires=['libvirt-python'],
    entry_points={
        'console_scripts': [
            'virshpatcher=virshpatcher.main:main',
        ]
    })
