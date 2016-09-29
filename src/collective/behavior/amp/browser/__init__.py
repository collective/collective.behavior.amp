# -*- coding: utf-8 -*-
"""View and viewlet used on this package."""
from collective.behavior.amp.behaviors import IAMP
from collective.behavior.amp.interfaces import IAMPSettings
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class AMPView(BrowserView):

    """Accelerated Mobile Pages default view."""

    index = ViewPageTemplateFile('view.pt')

    def __call__(self):
        return self.index()

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
