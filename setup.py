#!/usr/bin/env python
#-*- coding:utf-8 -*-


from setuptools import setup, find_packages

setup(
    name = "yt-ovs",
    version = "1.0.0",
    keywords = ("ovsdb","client","ovn"),
    description = "GUI tools show ovsdb",
    license = "MIT",

    url = "https://github.com/cao19881125/YtOvs.git",
    author = "yuntao.cao",
    author_email = "yuntao.cao@nocsys.com.cn",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['ovs'],
    scripts=['tools/yt-ovs']
)
