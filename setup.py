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
    version='0.4',
    description='coupledinput XBlock',   # TODO: write a better description.
    license='AGPL v3',          # TODO: choose a license: 'AGPL v3' and 'Apache 2.0' are popular.
    url="https://github.com/sodrew/coupledinput",
    packages=setuptools.find_packages(),
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'coupledinput = coupledinput:CoupledInputXBlock',
        ],
        "lms.djangoapp": [
            "coupledinput = coupledinput.apps:CoupledInputConfig",
        ],
    },
    package_data=package_data("coupledinput", ["static", "public", "migrations"]),
)
