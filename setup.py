from setuptools import setup, find_packages

setup(
    name='okscraper',
    version='0.0.5',
    description='module for scraping websites and documents',
    author='Ori Hoch',
    author_email='ori@uumpa.com',
    license='GPLv3',
    url='https://github.com/hasadna/okscraper',
    packages=find_packages(exclude=['tests', 'tests.*'])
)