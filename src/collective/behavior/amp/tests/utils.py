# -*- coding: utf-8 -*-
from plone.dexterity.interfaces import IDexterityFTI
from plone.formwidget.namedfile.converter import b64encode_file
from zope.component import queryUtility

import os


def enable_amp_behavior(portal_type):
    """Enable AMP behavior on the specified portal type."""
    fti = queryUtility(IDexterityFTI, name=portal_type)
    behavior = 'collective.behavior.amp.behaviors.IAMP'
    if behavior in fti.behaviors:
        return
    behaviors = list(fti.behaviors)
    behaviors.append(behavior)
    fti.behaviors = tuple(behaviors)


def get_file(filename):
    """Return contents of file from current directory."""
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, filename)
    with open(path, 'rb') as f:
        return f.read()


def get_file_b64encoded(filename):
    """Load file from current directory and return it b64encoded."""
    data = get_file(filename)
    return b64encode_file(filename, data)
