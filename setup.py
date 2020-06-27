"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='ezrealbot',  # Required
    version='1.0a2',  # Required
    description='A Discord bot project over the League of Legends thematics.',
    long_description='Through different commands users will call the bot for displaying some simple statistics, '
                     'funny facts, quotes from the game, etc. '
                     'The project aim to exploit Machine Learning model to realize his tasks.',
    long_description_content_type='text/markdown',
    url='https://github.com/maximeheliot/ezrealbot',
    author='An aspiring data scientist enthousiast',
    author_email='maxime.heliotpro@example.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Customer Service",
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='discordbot, discord, leagueoflegends',
    package_dir={'': 'ezrealbot'},
    packages=find_packages(where='ezrealbot'),
    python_requires='>=3.7, <4',
    install_requires=['discord.py',
                      'apscheduler',
                      'emoji'],
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/maximeheliot/ezrealbot/issues',
        'Funding': 'https://donate.pypi.org',
        'Source': 'https://github.com/maximeheliot/ezrealbot',
    },
)