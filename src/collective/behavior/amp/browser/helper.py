# -*- coding: utf-8 -*-
"""Helper view to access the publisher logo."""
from collective.behavior.amp.interfaces import IAMPSettings
from plone import api
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.browser import Download
from plone.namedfile.file import NamedImage


class PublisherLogoDownload(Download):

    """Helper view to return publisher logo data."""

    def __init__(self, context, request):
        super(PublisherLogoDownload, self).__init__(context, request)
        self.filename, self.data = None, None

        publisher_logo = api.portal.get_registry_record(
            IAMPSettings.__identifier__ + '.publisher_logo')

        if publisher_logo is not None:
            # set publisher logo data for download
            filename, data = b64decode_file(publisher_logo)
            data = NamedImage(data=data, filename=filename)
            self.filename, self.data = filename, data

    def _getFile(self):
        return self.data
