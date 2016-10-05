# -*- coding: utf-8 -*-
"""View and viewlet used on this package."""
from collections import OrderedDict
from collective.behavior.amp.behaviors import IAMP
from collective.behavior.amp.config import HAS_SOCIALLIKE
from collective.behavior.amp.config import IS_PLONE_5
from collective.behavior.amp.config import SOCIAL_SHARE_PROVIDERS
from collective.behavior.amp.interfaces import IAMPSettings
from collective.behavior.amp.utils import Html2Amp
from cStringIO import StringIO
from PIL import Image
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.textfield.interfaces import IRichTextValue
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.file import NamedBlobImage
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import json
import pkg_resources

try:
    pkg_resources.get_distribution('plone.app.relationfield')
except pkg_resources.DistributionNotFound:
    HAS_RELATIONFIELD = False
else:
    from plone.app.relationfield.behavior import IRelatedItems
    HAS_RELATIONFIELD = True

if HAS_SOCIALLIKE:
    from sc.social.like.interfaces import ISocialLikeSettings


class AMPView(BrowserView):

    """Accelerated Mobile Pages default view."""

    index = ViewPageTemplateFile('view.pt')

    def setup(self):
        try:
            self.sociallike = api.content.get_view(
                name='sl_helper', context=self.context, request=self.request)
        except api.exc.InvalidParameterError:
            self.sociallike = None

    def __call__(self):
        self.setup()
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
    def has_sociallike(self):
        """Check if sc.social.like is installed and enabled."""
        if self.sociallike is None:
            return False
        return self.sociallike.enabled() and self.sociallike.plugins()

    @property
    def share_buttons(self):
        """Return the list of social networks enabled."""
        # this code is executed only if sc.social.like is installed
        plugins = [i.id for i in self.sociallike.plugins()]
        return [i for i in plugins if i in SOCIAL_SHARE_PROVIDERS]

    @property
    def facebook_app_id(self):
        """Return the Facebook app_id configured."""
        # this code is executed only if sc.social.like is installed
        app_id = ISocialLikeSettings.__identifier__ + '.facebook_app_id'
        return api.portal.get_registry_record(app_id)

    @property
    def lead_image(self):
        """Return lead image information, if present. We try to guess
        the information based on field names as it's useless to try
        to deal with the ILeadImage interface.
        :returns: lead image information
        :rtype: dict or None
        """
        image = getattr(self.context, 'image', None)
        if image is None:
            return None  # no "image" field

        if not isinstance(image, NamedBlobImage):
            return None  # not a real image

        url = '{0}/@@download/image/{1}'.format(
            self.context.absolute_url(), image.filename)
        caption = getattr(self.context, 'image_caption', None)
        width, height = image.getImageSize()
        return dict(url=url, caption=caption, width=width, height=height)

    @property
    def amp_analytics(self):
        amp_analytics = IAMPSettings.__identifier__ + '.amp_analytics'
        return api.portal.get_registry_record(amp_analytics)

    @property
    def text(self):
        if not getattr(self.context, 'text', False):
            return
        if not IRichTextValue.providedBy(self.context.text):
            return
        util = Html2Amp()
        return util(self.context.text.output)

    def get_listing_view_action(self, item):
        """Return the item's view action used in listings.
        :param item: the item to be processed
        :type item: catalog brain
        :returns: the item's view action
        :rtype: str
        """
        if IS_PLONE_5:
            registry = api.portal.get_tool('portal_registry')
            use_view_action = registry.get(
                'plone.types_use_view_action_in_listings', [])
        else:
            portal_properties = api.portal.get_tool('portal_properties')
            site_properties = portal_properties.site_properties
            use_view_action = site_properties.getProperty(
                'typesUseViewActionInListings', [])

        # types that use view action need to add '/view' to its canonical URL
        url = item.getURL()
        if item.portal_type in use_view_action:
            return url + '/view'
        return url

    def related_items(self):
        """Return the items related with the current object.
        :returns: list of catalog brains
        """
        res = ()
        if HAS_RELATIONFIELD and IRelatedItems.providedBy(self.context):
            relations = self.context.relatedItems
            if not relations:
                return ()
            res = self.relations2brains(relations)

        return res

    def relations2brains(self, relations):
        """Return a list of brains based on a list of relations. Will filter
        relations if the user has no permission to access the content.
        :param relations: object relations
        :type relations: list
        :returns: catalog brains
        :rtype: list
        """
        catalog = api.portal.get_tool('portal_catalog')
        brains = []
        for item in relations:
            path = item.to_path
            # the query will return an empty list if the user has no
            # permission to see the target object
            brains.extend(catalog(path=dict(query=path, depth=0)))
        return brains


class AMPViewlet(ViewletBase):

    """Accelerated Mobile Pages default viewlet."""

    @property
    def enabled(self):
        if IAMP.providedBy(self.context):
            return True
