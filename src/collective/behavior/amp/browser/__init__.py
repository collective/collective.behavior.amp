# -*- coding: utf-8 -*-
"""View and viewlet used on this package."""
from collections import OrderedDict
from collective.behavior.amp.behaviors import IAMP
from collective.behavior.amp.interfaces import IAMPSettings
from cStringIO import StringIO
from PIL import Image
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from plone.formwidget.namedfile.converter import b64decode_file
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import json


class AMPView(BrowserView):

    """Accelerated Mobile Pages default view."""

    index = ViewPageTemplateFile('view.pt')

    def __call__(self):
        return self.index()

    @property
    def publisher_logo(self):
        """Return publisher logo information as a dictionary."""
        publisher_logo = api.portal.get_registry_record(
            IAMPSettings.__identifier__ + '.publisher_logo')

        if publisher_logo is None:
            return None

        portal_url = api.portal.get().absolute_url()
        filename, data = b64decode_file(publisher_logo)
        width, height = Image.open(StringIO(data)).size

        return dict(
            url='{0}/@@amp-publisher-logo/{1}'.format(portal_url, filename),
            width=width,
            height=height,
        )

    @property
    def metadata(self):
        """Return metadata as structured data in JSON-LD format. All
        fields are required except for mainEntityOfPage, dateModified
        and description.

        More information:
        https://developers.google.com/search/docs/data-types/articles

        Validation:
        https://search.google.com/structured-data/testing-tool
        """
        # use an OrderedDict to make the output human readable
        metadata = OrderedDict()
        metadata['@context'] = 'http://schema.org'
        metadata['@type'] = 'NewsArticle'

        metadata['mainEntityOfPage'] = self.context.absolute_url()  # canonical URL
        metadata['headline'] = self.context.Title()

        # TODO: lead image
        # metadata['image'] = OrderedDict()
        # metadata['image']['@type'] = 'ImageObject'
        # metadata['image']['url'] = 'https://google.com/thumbnail1.jpg'
        # metadata['image']['height'] = 800
        # metadata['image']['width'] = 800

        metadata['publisher'] = OrderedDict()
        metadata['publisher']['@type'] = 'Organization'
        metadata['publisher']['name'] = api.portal.get().Title()

        if self.publisher_logo is not None:
            metadata['publisher']['logo'] = OrderedDict()
            metadata['publisher']['logo']['@type'] = 'ImageObject'
            metadata['publisher']['logo']['url'] = self.publisher_logo['url']
            metadata['publisher']['logo']['width'] = self.publisher_logo['width']
            metadata['publisher']['logo']['height'] = self.publisher_logo['height']

        metadata['datePublished'] = self.context.effective().ISO8601()
        metadata['dateModified'] = self.context.modified().ISO8601()

        metadata['author'] = OrderedDict()
        metadata['author']['@type'] = 'Person'
        metadata['author']['name'] = self.author

        metadata['description'] = self.context.Description()
        return json.dumps(metadata, indent=2)

    @property
    def portal_tabs(self):
        """Return the list of portal tabs by calling a helper view."""
        portal_tabs_view = api.content.get_view(
            name='portal_tabs_view', context=self.context, request=self.request)
        return portal_tabs_view.topLevelTabs()

    @property
    def show_byline(self):
        # TODO: honor privacy settings
        return True

    @property
    def author(self):
        # TODO: generalize
        return self.context.Creator()

    @property
    def published(self):
        """Return publication date, if available."""
        return getattr(self.context, 'effective_date', None)

    def get_localized_time(self, datetime):
        """Convert time into localized time in long format."""
        return api.portal.get_localized_time(datetime, long_format=True)

    @property
    def amp_analytics(self):
        amp_analytics = IAMPSettings.__identifier__ + '.amp_analytics'
        return api.portal.get_registry_record(amp_analytics)


class AMPViewlet(ViewletBase):

    """Accelerated Mobile Pages default viewlet."""

    @property
    def enabled(self):
        if IAMP.providedBy(self.context):
            return True
