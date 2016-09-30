# -*- coding: utf-8 -*-
from collective.behavior.amp import _
from collective.behavior.amp.validators import is_json
from collective.behavior.amp.validators import is_valid_logo
from plone.autoform import directives as form
from plone.formwidget.namedfile.widget import NamedImageFieldWidget
from plone.supermodel import model
from zope import schema
from zope.interface import Interface


class IAddOnLayer(Interface):

    """A layer specific for this add-on product."""


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

    form.widget('amp_analytics', rows=15)
    amp_analytics = schema.Text(
        title=_(u'AMP Analytics'),
        description=_(
            u'The value (in JSON-LD format) of the "amp-analytics" element '
            u'that will be used to measure activity on AMP documents.'
        ),
        required=False,
        default=u'',
        constraint=is_json,
    )
