# -*- coding: utf-8 -*-
"""View and viewlet used on this package."""
from collective.behavior.amp.behaviors import IAMP
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class AMPView(BrowserView):

    """Accelerated Mobile Pages default view."""

    index = ViewPageTemplateFile('view.pt')

    def __call__(self):
        return self.index()


class AMPViewlet(ViewletBase):

    """Accelerated Mobile Pages default viewlet."""

    @property
    def enabled(self):
        if IAMP.providedBy(self.context):
            return True
