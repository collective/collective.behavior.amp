# -*- coding: utf-8 -*-
"""Event subscribers."""
from collective.behavior.amp.logger import logger
from plone import api
from urlparse import urlparse

import requests


def validate_amp(obj, event):
    """Validate @@amp view using Cloudflare's AMP linter API endpoint."""
    request = obj.REQUEST

    if event.status['review_state'] not in ('published', ):
        return

    # remove the scheme from the URL
    url = ''.join(urlparse(obj.absolute_url())[1:])

    r = requests.get('https://amp.cloudflare.com/q/' + url + '/@@amp')
    validation = r.json()

    if validation['valid']:
        msg = u'Valid AMP page'
        logger.info(msg)
        api.portal.show_message(message=msg, request=request, type='info')
    else:
        msg = u'Not a valid AMP page'
        logger.warn(msg)
        api.portal.show_message(message=msg, request=request, type='warn')

        # TODO: include information about the errors
