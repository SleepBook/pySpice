from setuptools import setup

setup(
    author = 'Wenqi Yin',
    version = '0.1',
    description = 'spice simulator implemented in python',
    install_requires = ['nose', 'numpy','matplotlib','getopt'],
    packages = ['pySpice'],
    scripts = ['bin/pyspice','bin/result_viewer'],
    name = 'pySpice'
    )
