# -*- coding: utf-8 -*-
"""Setup testing fixture.

For Plone 5 we need to install plone.app.contenttypes.

Social share feature is only tested in Plone 4.3.
"""
from collective.behavior.amp.config import HAS_SOCIALLIKE
from plone import api
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.dexterity.interfaces import IDexterityFTI
from plone.testing import z2
from zope.component import queryUtility

IS_PLONE_5 = api.env.plone_version().startswith('5')


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        if HAS_SOCIALLIKE:
            import sc.social.like
            self.loadZCML(package=sc.social.like)

        import collective.behavior.amp
        self.loadZCML(package=collective.behavior.amp)

    def setUpPloneSite(self, portal):
        if HAS_SOCIALLIKE:
            self.applyProfile(portal, 'sc.social.like:default')

        self.applyProfile(portal, 'collective.behavior.amp:default')
        self._enable_amp_behavior('News Item')
        portal.portal_workflow.setDefaultChain('one_state_workflow')

    def _enable_amp_behavior(self, portal_type):
        """Enable AMP behavior on the specified portal type."""
        fti = queryUtility(IDexterityFTI, name=portal_type)
        behavior = 'collective.behavior.amp.behaviors.IAMP'
        if behavior in fti.behaviors:
            return
        behaviors = list(fti.behaviors)
        behaviors.append(behavior)
        fti.behaviors = tuple(behaviors)


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='collective.behavior.amp:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='collective.behavior.amp:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='collective.behavior.amp:Robot',
)
