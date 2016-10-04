from setuptools import setup, find_packages

setup(
    author = 'Wenqi Yin',
    author_email = 'oar.yin@sjtu.edu.cn',
    url = 'url',
    license = 'MIT',
    version = '0.1',
    description = 'spice simulator implemented in python',
    install_requires = ['nose', 'numpy','matplotlib'],
    packages = find_packages(),
	package_data = {'pySpice': ['data/sample_netlist/*.sp']},
    scripts = ['bin/pyspice','bin/result_viewer'],
    name = 'pySpice'
    )
