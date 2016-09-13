# -*- coding: utf-8 -*-
from collective.behavior.amp import _  # noqa
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema  # noqa
from zope.interface import provider


@provider(IFormFieldProvider)
class IAMP(model.Schema):

    """Accelerated Mobile Pages behavior."""
