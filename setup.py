from setuptools import setup

setup(
    author = 'Wenqi Yin',
    author_email = 'oar.yin@sjtu.edu.cn',
    url = 'url',
    license = 'MIT',
    version = '0.1',
    description = 'spice simulator implemented in python',
    install_requires = ['nose', 'numpy','matplotlib','getopt'],
    packages = ['pySpice','test'],
    scripts = ['bin/pyspice','bin/result_viewer'],
    name = 'pySpice'
    )
