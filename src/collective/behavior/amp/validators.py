# -*- coding: utf-8 -*-
from collective.behavior.amp import _
from cStringIO import StringIO
from PIL import Image
from plone.formwidget.namedfile.converter import b64decode_file
from zope.interface import Invalid

import json


def is_json(value):
    """Checks if value contains a valid JSON string."""
    if value == u'':
        return True

    try:
        json.loads(value)
        return True
    except ValueError:
        return False


def is_valid_logo(value):
    """Check if the image is a valid logo:

    * Logos should have a wide aspect ratio, not a square icon
    * Logos should be no wider than 600px, and no taller than 60px
    """
    if not value:
        return True

    filename, data = b64decode_file(value)
    width, height = Image.open(StringIO(data)).size

    if width <= height:
        raise Invalid(_(u'Image should have a wide aspect ratio.'))

    if width > 600 or height > 60:
        raise Invalid(_(
            u'Image should be no wider than 600px, and no taller than 60px.'))

    return True
