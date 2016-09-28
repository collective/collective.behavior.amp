# -*- coding: utf-8 -*-
from collective.behavior.amp import _
from collective.behavior.amp.validators import isJSON
from plone.autoform import directives as form
from plone.supermodel import model
from zope import schema
from zope.interface import Interface


class IAddOnLayer(Interface):

    """A layer specific for this add-on product."""


class IAMPSettings(model.Schema):

    """Schema for the control panel form."""

    form.widget('amp_analytics', rows=15)
    amp_analytics = schema.Text(
        title=_(u'AMP Analytics'),
        description=_(
            u'The value (in JSON-LD format) of the "amp-analytics" element '
            u'that will be used to measure activity on AMP documents.'
        ),
        required=False,
        default=u'',
        constraint=isJSON,
    )
