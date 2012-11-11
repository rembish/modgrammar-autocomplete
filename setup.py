from setuptools import setup, find_packages
from modautocomplete import __version__

setup(
    name='modautocomplete',
    version=__version__,
    download_url='https://github.com/don-ramon/modgrammar-autocomplete',
    license='BSD',
    author='Aleksey Rembish',
    author_email='alex@rembish.ru',
    description='Autocomplete support for modgrammar-py2',
    packages=find_packages(),
    install_requires=[
        'modgrammar-py2',
    ],
    long_description='TODO',
    classifiers=[
        # TODO
    ]
)
