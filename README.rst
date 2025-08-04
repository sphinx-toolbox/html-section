#############
html-section
#############

.. start short_desc

**Sphinx extension to hide section headers with non-HTML builders.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |actions_linux| image:: https://github.com/sphinx-toolbox/html-section/workflows/Linux/badge.svg
	:target: https://github.com/sphinx-toolbox/html-section/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/sphinx-toolbox/html-section/workflows/Windows/badge.svg
	:target: https://github.com/sphinx-toolbox/html-section/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/sphinx-toolbox/html-section/workflows/macOS/badge.svg
	:target: https://github.com/sphinx-toolbox/html-section/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/sphinx-toolbox/html-section/workflows/Flake8/badge.svg
	:target: https://github.com/sphinx-toolbox/html-section/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/sphinx-toolbox/html-section/workflows/mypy/badge.svg
	:target: https://github.com/sphinx-toolbox/html-section/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/sphinx-toolbox/html-section/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/sphinx-toolbox/html-section/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/sphinx-toolbox/html-section/master?logo=coveralls
	:target: https://coveralls.io/github/sphinx-toolbox/html-section?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/sphinx-toolbox/html-section?logo=codefactor
	:target: https://www.codefactor.io/repository/github/sphinx-toolbox/html-section
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/html-section
	:target: https://pypi.org/project/html-section/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/html-section?logo=python&logoColor=white
	:target: https://pypi.org/project/html-section/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/html-section
	:target: https://pypi.org/project/html-section/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/html-section
	:target: https://pypi.org/project/html-section/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/sphinx-toolbox/html-section
	:target: https://github.com/sphinx-toolbox/html-section/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/sphinx-toolbox/html-section
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/sphinx-toolbox/html-section/v0.4.0
	:target: https://github.com/sphinx-toolbox/html-section/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/sphinx-toolbox/html-section
	:target: https://github.com/sphinx-toolbox/html-section/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2025
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/html-section
	:target: https://pypi.org/project/html-section/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``html-section`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install html-section

.. end installation

Then enable the extension by adding the following to your ``conf.py`` file:

.. code-block:: python

	extensions = [
			...,  # Other extensions go here
			"html_section",
			]


Usage
---------

.. code-block:: rest

	Contents
	-----------

	.. html-section::

The section label ``Contents`` will only be shown with the HTML builder.
However, the section content will still be visible, and the heading will appear in the table of contents.
Consider using Sphinx's ``.. only:: html`` directive for that.


.. code-block:: rest

	Contents
	-----------

	.. latex-section::

The section label ``Contents`` will only be shown with the LaTeX builder.
However, the section content will still be visible, and the heading will appear in the table of contents.
Consider using Sphinx's ``.. only:: latex`` directive for that.

*New in version 0.4.0*


.. code-block:: rest

	Contents
	-----------

	.. phantom-section::

The section label ``Contents`` will be hidden with all builders,
but the section will still exist in the structure of the document
(i.e. a new section will be started, without a label).
The section content will still be visible, and the heading will appear in the table of contents.
