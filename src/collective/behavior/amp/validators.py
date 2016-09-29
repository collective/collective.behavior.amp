# -*- coding: utf-8 -*-
import json


def isJSON(value):
    """Checks if value contains a valid JSON string."""
    if value == u'':
        return True

    try:
        json.loads(value)
        return True
    except ValueError:
        return False
