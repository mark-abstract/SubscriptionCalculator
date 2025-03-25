#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 00:13:21 2025

@author: wesski84
"""
import sys
sys.setrecursionlimit(5000)

from setuptools import setup

APP = ['SubscriptionCalculator.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'excludes': ['tomli'],
    # any other options you need...
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)