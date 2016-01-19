from setuptools import setup, find_packages
from os import path

setup(
    name='mailshooter',
    version='0.0.1',
    description='mailshooter',
    install_requires=[
        'mako>=1.0.1,<1.1',
        'PyYAML==3.11',
    ],
    entry_points={
        'console_scripts': [
            'mailshooter=bin.mailshooter:main',
        ]
    },
)
