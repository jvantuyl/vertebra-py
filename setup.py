#!/usr/bin/env python2.6
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

setup(
  name="vertebra-py",
  version='0.1.0',
  description="Vertebra Agent Library for Python",
  author="Jayson Vantuyl",
  author_email="jvantuyl@engineyard.com",
  url="http://vertebra.engineyard.com",
  package_dir = {'': 'lib'},
  packages=[
    'vertebra',
    'vertebra.actors',
    'vertebra.conn',
    'vertebra.conn.xmpp',
    'vertebra.util',
  ],
  scripts=['bin/agent'],
  test_suite='nose.collector',
  provides=['vertebra (0.1)'],
  requires=[
    'sys(>=2.6)',
    'pyxmpp(>=1.6.0)',
    'fibra(>=0.0.10)',
    'yaml(>=3.0)',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: No Input/Output (Daemon)',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: Unix',
    'Programming Language :: Python :: 2.6',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: System :: Distributed Computing',
  ],
)
