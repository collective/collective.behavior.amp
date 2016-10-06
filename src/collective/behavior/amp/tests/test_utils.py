# -*- coding: utf-8 -*-
from collective.behavior.amp.testing import INTEGRATION_TESTING
from collective.behavior.amp.tests.utils import get_file
from collective.behavior.amp.utils import Html2Amp
from lxml import html
from plone import api
from plone.namedfile.file import NamedBlobImage

import unittest


class Html2AmpTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.util = Html2Amp()

        filename = u'logo-plone-ok.png'
        data = get_file(filename)
        with api.env.adopt_roles(['Manager']):
            self.image = api.content.create(
                container=self.portal,
                type='Image',
                title='foo',
                image=NamedBlobImage(data=data, filename=filename)
            )

    def test_transform_img_tags(self):
        code = '<img class="foo" src="resolveuid/{0}" />'
        el = html.fromstring(code.format(self.image.UID()))
        self.util.transform_img_tags(el)
        self.assertEqual(el.tag, 'amp-img')
        self.assertEqual(el.attrib['src'], 'http://nohost/plone/foo')
        self.assertEqual(el.attrib['width'], '231')
        self.assertEqual(el.attrib['height'], '60')
        self.assertEqual(el.attrib['layout'], 'responsive')
        self.assertNotIn('class', el.attrib)

    def test_remove_invalid_tags(self):
        code = (
            '<div>'
            '<img src="/foo.jpg" width="800" height="600" />'
            '<iframe src="/bar" width="800" height="600" /></iframe>'
            '</div>'
        )
        el = html.fromstring(code)
        self.util.remove_invalid_tags(el)
        self.assertEqual(html.tostring(el), '<div></div>')

    def test_utility(self):
        code = (
            '<p>Lorem ipsum.</p>'
            '<img class="foo" src="resolveuid/{0}" />'
            '<iframe src="/bar" width="800" height="600" /></iframe>'
            '<p>Neque porro.</p>'
        ).format(self.image.UID())
        expected = (
            '<div class="amp-text">'
            '<p>Lorem ipsum.</p>'
            '<amp-img src="http://nohost/plone/foo" width="231" height="60" layout="responsive"></amp-img>'
            '<p>Neque porro.</p>'
            '</div>'
        )
        self.assertEqual(self.util(code), expected)
