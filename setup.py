from numpy import maximum
from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt', 'r') as req:
        content = req.read()
        requirements = content.split('\n')

    return requirements

setup(
    name='notion-cli',
    version='0.0.1',
    author="cebosithole",
    description="CLI for notion, with various tools for interacting with notion",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=read_requirements(),

    entry_points="""
        [console_scripts]
        notion-cli=cli:main_cli
    """
)
