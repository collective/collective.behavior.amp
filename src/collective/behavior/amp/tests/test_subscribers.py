# -*- coding: utf-8 -*-
from collective.behavior.amp.testing import INTEGRATION_TESTING
from plone import api
from Products.statusmessages.interfaces import IStatusMessage

import requests_mock
import unittest


class AMPValidationTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        with api.env.adopt_roles(['Manager']):
            self.obj = api.content.create(self.portal, 'News Item', 'foo')

    @requests_mock.mock()
    def test_validate_amp_valid(self, m):
        RESPONSE_VALID = """{"source":"http://nohost/plone/foo/@@amp","valid":true}"""
        m.get('https://amp.cloudflare.com/q/nohost/plone/foo/@@amp', text=RESPONSE_VALID)

        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.obj, 'publish')

        messages = IStatusMessage(self.request).show()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, u'Valid AMP page')
        self.assertEqual(messages[0].type, u'info')

    @requests_mock.mock()
    def test_validate_amp_invalid(self, m):
        RESPONSE_INVALID = """{"source":"http://nohost/plone/foo/@@amp","valid":false,"errors":[{"line":169,"col":0,"code":"GENERAL_DISALLOWED_TAG","error":"The tag 'script' is disallowed except in specific forms."}]}"""
        m.get('https://amp.cloudflare.com/q/nohost/plone/foo/@@amp', text=RESPONSE_INVALID)

        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.obj, 'publish')

        messages = IStatusMessage(self.request).show()
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, u'Not a valid AMP page')
        self.assertEqual(messages[0].type, u'warn')

    @unittest.expectedFailure  # FIXME
    def test_validate_amp_with_package_uninstalled(self):
        from collective.behavior.amp.config import PROJECTNAME
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])

        # don't fail if package uninstalled
        with api.env.adopt_roles(['Manager']):
            api.content.transition(self.obj, 'publish')
