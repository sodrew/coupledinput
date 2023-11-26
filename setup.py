"""Setup for coupledinput XBlock."""


import os

from setuptools import setup
import setuptools

# https://github.com/tony-h/rocketchat-tab/blob/main/setup.py

def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='coupledinput',
    version='0.12',
    description='XBlock that enables two responders to questions in a course',
    license='AGPL v3',
    url="https://github.com/sodrew/coupledinput",
    packages=setuptools.find_packages(),
    install_requires=[
        'XBlock',
        'unicodecsv',
    ],
    entry_points={
        'xblock.v1': [
            'coupledinput = coupledinput:CoupledInputXBlock',
        ],
        "lms.djangoapp": [
            "coupledinput = coupledinput.apps:CoupledInputConfig",
        ],
    },
    package_data=package_data("coupledinput",
                              ["static", "public", "migrations"]),
)
