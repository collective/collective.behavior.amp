# -*- coding: utf-8 -*-
from collective.behavior.amp import _
from collective.behavior.amp.interfaces import IAMPSettings
from plone.app.registry.browser import controlpanel


class AMPSettingsEditForm(controlpanel.RegistryEditForm):

    """Control panel edit form."""

    schema = IAMPSettings
    label = _(u'Accelerated Mobile Pages')
    description = _(u'Settings for AMP integration.')


class AMPSettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    """Control panel form wrapper."""

    form = AMPSettingsEditForm
