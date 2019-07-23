#!/usr/bin/env python
import setuptools

setuptools.setup(
    name                = 'hello_chatwork',
    version             = '1.0.0',
    packages            = setuptools.find_packages(),
    author              = 'Tooru TSURUKAWA',
    author_email        = 'rockbone.g@gmail.com',
    description         = 'Hello Chatwork! Please show me log!',
    long_description    = 'file:README.md',
    url                 = 'https://github.com/rockbone/hello_chatwork',
    license             = 'Apache License, Version 2.0',
    install_requires    = [
        'requests',
        'argparse',
        'datetime',
        'inquirer',
        'requests',
    ],
    entry_points        = {
        'console_scripts':[
            'hello_chatwork = hello_chatwork.hello_chatwork:main',
        ],
    },
)
