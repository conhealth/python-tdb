Python package for Sambas TDB (trivial database) bindings
=========================================================

Samba offers Python bindings for TDB (trivial database) files. Usually these
are distributed together with Samba through the packaging system of Linux
distributions. For Debian based distributions they are for example part of
the ``python-tdb`` debian package.

Those work fine when running Python in the default environment, but when you
have a virtualenv without inherited system site packages, you have no access to
it. This project solves this issue, by providing a python packaging solution
for generation the TDB bindings.

Installation and Usage
----------------------

- Ensure you have ``libtdb-dev`` installed.
- Clone the repository
- To compile the c-extension for the bindings just run the usual package
  building commands like:

  python setup.py bdist_wheel sdist
