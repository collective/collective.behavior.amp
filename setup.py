# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '1.0b2.dev0'
description = 'Support for Accelerated Mobile Pages (AMP) on Dexterity-based content types.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(
    name='collective.behavior.amp',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Office/Business :: News/Diary',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone amp dexterity behavior',
    author='Simples Consultoria',
    author_email='produtos@simplesconsultoria.com.br',
    url='https://github.com/collective/collective.behavior.amp',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['collective', 'collective.behavior'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'plone.app.layout',
        'plone.app.registry',
        'plone.autoform',
        'plone.behavior',
        'plone.dexterity',
        'plone.supermodel',
        'Products.CMFCore',
        'Products.CMFPlone >=4.3',
        'Products.GenericSetup',
        'setuptools',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'AccessControl',
            'plone.app.contenttypes',
            'plone.app.robotframework',
            'plone.app.testing [robot]',
            'plone.browserlayer',
            'plone.registry',
            'plone.testing',
            'robotsuite',
            'zope.component',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
