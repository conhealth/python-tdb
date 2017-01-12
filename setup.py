#!/usr/bin/env python

from __future__ import print_function

import os
import shutil
import subprocess
import sys
import tarfile
import tempfile

from setuptools import setup
from setuptools.extension import Extension

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


# TDB version to build the extension for
VERSION = '1.3.12'

tmp_dir = tempfile.mkdtemp()
build_dir = os.path.join(tmp_dir, 'tdb-{}'.format(VERSION))
download_base_path = 'https://www.samba.org/ftp/tdb/'
download_file_name = 'tdb-{}.tar.gz'.format(VERSION)
download_location = os.path.join(tmp_dir, download_file_name)

try:
    urlretrieve('{}/{}'.format(download_base_path, download_file_name),
                download_location)
except Exception:
    shutil.rmtree(tmp_dir)
    print('Retrieving the tdb sources failed.')
    print('Check your internet connectivity.')
    sys.exit(1)

try:
    tar_file = tarfile.open(download_location)
    tar_file.extractall(path=tmp_dir)
    tar_file.close()
except tarfile.TarError:
    shutil.rmtree(tmp_dir)
    print('Extracting tdb sources failed')
    sys.exit(1)

proc = subprocess.Popen(['./configure'], cwd=build_dir)
proc.communicate()
if proc.returncode != 0:
    shutil.rmtree(tmp_dir)
    print('Configuring tdb failed.')
    sys.exit(1)

module1 = Extension('tdb',
                    [os.path.join(build_dir, 'pytdb.c')],
                    extra_compile_args=['-DPACKAGE_VERSION="{}"'.format(VERSION)],
                    include_dirs=[os.path.join(build_dir, 'lib/replace'),
                                  os.path.join(build_dir, 'bin/default'),
                                  os.path.join(build_dir, 'common'),
                                  os.path.join(build_dir, 'include')],
                    libraries=['tdb'],
                    runtime_library_dirs=['/usr/lib/', '/usr/local/lib'],
                    )

setup(name='tdb',
      version=VERSION,
      description='Python package for Sambas TDB (trivial database) bindings',
      license='LGPLv3+',
      maintainer='Daniel Roschka',
      maintainer_email='daniel.roschka@connected-health.eu',
      url='https://www.github.com/conhealth/python-tdb',
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
      ],
      ext_modules=[module1])

shutil.rmtree(tmp_dir)
