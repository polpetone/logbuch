from setuptools import setup, find_packages

setup(
    name='logbuch',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'jsonpickle',
        'pyyaml'
    ],
    entry_points='''
        [console_scripts]
        logbuch=logbuch.portadapter.commands.cli:cli
    ''',
)
