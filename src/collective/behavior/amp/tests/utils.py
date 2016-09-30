# -*- coding: utf-8 -*-
from plone.formwidget.namedfile.converter import b64encode_file

import os


def load_b64encoded_image(filename):
    """Load file from current directory and return it b64encoded."""
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, filename)
    with open(path, 'rb') as f:
        data = f.read()
    return b64encode_file(filename, data)
