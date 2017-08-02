# -*- coding: utf-8 -*-
from collective.behavior.amp import _
from collective.behavior.amp.config import AMP_STICKY_AD_PLACEHOLDER
from collective.behavior.amp.validators import is_valid_logo
from collective.behavior.amp.validators import is_xml
from plone.autoform import directives as form
from plone.formwidget.namedfile.widget import NamedImageFieldWidget
from plone.supermodel import model
from zope import schema
from zope.interface import Interface


class IAddOnLayer(Interface):

    """A layer specific for this add-on product."""


class IAMPPixelProvider(Interface):
    """Adapter for amp-pixel tags."""

    def pixel(self):
        """Return amp-pixel tag if available."""


class IAMPSettings(model.Schema):

    """Schema for the control panel form."""

    form.widget('publisher_logo', NamedImageFieldWidget)
    publisher_logo = schema.ASCII(
        title=_(u'Publisher Logo'),
        description=_(
            u'The logo of the publisher. Should have a wide aspect ratio, '
            u'and should be no wider than 600px, and no taller than 60px.'
        ),
        required=False,
        constraint=is_valid_logo,
    )

    # XXX: placeholder attribute is not working
    form.widget('amp_sticky_ad', rows=15, placeholder=AMP_STICKY_AD_PLACEHOLDER)
    amp_sticky_ad = schema.Text(
        title=_(u'AMP Sticky Ad'),
        description=_(
            u'Adds support for ad units that always take a fixed place in the viewport. '
            u'Fill with the "amp-ad" element that will be used as a direct child of "amp-sticky-ad". '
            u'See <a href="https://ampbyexample.com/components/amp-sticky-ad/">amp-sticky-ad</a> for examples on how to implement this feature.'
        ),
        required=False,
        default=u'',
        constraint=is_xml,
    )

    form.widget('amp_analytics', rows=15)
    amp_analytics = schema.Text(
        title=_(u'AMP Analytics'),
        description=_(
            u'The "amp-analytics" elements that will be used to measure activity on AMP documents. '
            u'See <a href="https://developers.google.com/analytics/devguides/collection/amp-analytics/">'
            u'Adding Analytics to your AMP pages</a> for examples on how to implement this feature.'
        ),
        required=False,
        default=u'',
        constraint=is_xml,
    )
