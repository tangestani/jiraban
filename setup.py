#!/usr/bin/env python
import os
import re

#import ez_setup
#ez_setup.use_setuptools()

from setuptools import (
    find_packages,
    setup,
    )


if os.path.isfile("MANIFEST"):
    os.unlink("MANIFEST")


VERSION = re.search(
    r'version = "([^"]+)"',
    open("jiraban/__init__.py").read()).group(1)


setup(
    name="jiraban",
    version=VERSION,
    author="Marc Tardif",
    author_email="marc@interunion.ca",
    license="GPL",
    description="Generate a Kanban board from JIRA.",
    long_description="""
This is a simple tool to generate a Kanban board from data in JIRA.
""",
    packages=find_packages(),
    install_requires=[
        "jinja2",
        "requests",
        ],
    scripts=[
        "bin/jiraban",
        ],
    # The following options are specific to setuptools but ignored (with a
    # warning) by distutils.
    include_package_data=True,
    zip_safe=False,
    test_suite="jiraban.tests.find_tests",
    )
