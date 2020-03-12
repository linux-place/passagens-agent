#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements= [
    'docutils==0.14',
    "lockfile==0.12.2",
    "paho-mqtt==1.3.1",
    "pid==2.2.0",
    "python-daemon==2.1.2",
    "python-varnish==0.2.1",
    "service==0.5.1",
    "setproctitle==1.1.10",
    ]

setuptools.setup(name='passagens-agent',
    version='1.1.0',
    description='Daemon de gerenciamento de cache distribuido do passagens imperdiveis',
    author='Fernando Augusto Medeiros Silva',
    author_email='fams@linuxpalce.com.br',
    url='www.passagensimperdiveis.com.br',
    packages=setuptools.find_packages(),
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
         "Programming Language :: Python :: 2.7",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ),
    install_requires=requirements,
    scripts=[ 'bin/passagens-agent.py'],

     )
