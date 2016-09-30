# -*- coding: utf-8 -*-
from collective.behavior.amp.interfaces import IAMPSettings
from collective.behavior.amp.testing import INTEGRATION_TESTING
from collective.behavior.amp.tests.utils import load_b64encoded_image
from lxml import etree
from plone import api

import unittest


class AMPViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        with api.env.adopt_roles(['Manager']):
            self.newsitem = api.content.create(
                container=self.portal, type='News Item', title='Lorem Ipsum')

        # the view is registered in the context of the object
        self.view = api.content.get_view(
            name='amp', context=self.newsitem, request=self.request)

    def _get_metadata_as_json(self, html):
        # the text inside the script tag must be a valid JSON
        import json
        return json.loads(html.find('.//head/script').text)

    def test_metadata(self):
        amp = etree.HTML(self.view())
        self.assertEqual(
            amp.find('.//head/script').attrib['type'], 'application/ld+json')

        metadata = self._get_metadata_as_json(amp)
        self.assertEqual(metadata['@context'], u'http://schema.org')
        self.assertEqual(metadata['@type'], u'NewsArticle')
        self.assertEqual(
            metadata['mainEntityOfPage'], self.newsitem.absolute_url())
        self.assertEqual(metadata['headline'], self.newsitem.Title())

        # TODO: lead image
        self.assertNotIn('image', metadata)

        self.assertEqual(metadata['publisher']['@type'], u'Organization')
        self.assertEqual(metadata['publisher']['name'], u'Plone site')

        # no metadata present if logo not defined
        self.assertNotIn('logo', metadata['publisher'])
        # publisher logo is tested below

        self.assertEqual(
            metadata['datePublished'], self.newsitem.effective().ISO8601())
        self.assertEqual(
            metadata['dateModified'], self.newsitem.modified().ISO8601())

        self.assertEqual(metadata['author']['@type'], u'Person')
        self.assertEqual(metadata['author']['name'], u'test_user_1_')

        self.assertEqual(metadata['description'], self.newsitem.Description())

    def test_metadata_logo(self):
        # publisher logo information must be available if logo is loaded
        filename = 'logo-plone-ok.png'
        logo = load_b64encoded_image(filename)
        api.portal.set_registry_record(
            IAMPSettings.__identifier__ + '.publisher_logo', logo)

        amp = etree.HTML(self.view())
        metadata = self._get_metadata_as_json(amp)
        self.assertIn('logo', metadata['publisher'])

        metadata = metadata['publisher']['logo']  # shortcut
        self.assertEqual(metadata['@type'], u'ImageObject')
        url = u'http://nohost/plone/@@amp-publisher-logo/{0}'.format(filename)
        self.assertEqual(metadata['url'], url)
        self.assertEqual(metadata['width'], 231)
        self.assertEqual(metadata['height'], 60)

    def test_byline(self):
        # byline must contain the name of the author
        # and the last modification date only
        amp = etree.HTML(self.view())
        text = ''.join(amp.find('.//div[@class="amp-byline"]').itertext())
        self.assertIn('test_user_1_', text)
        self.assertNotIn('published', text)
        self.assertIn('last modified', text)

        # mark item as published
        from DateTime import DateTime
        self.newsitem.effective_date = DateTime()
        amp = etree.HTML(self.view())
        text = ''.join(amp.find('.//div[@class="amp-byline"]').itertext())
        self.assertIn('published', text)

    def test_amp_analytics(self):
        amp = etree.HTML(self.view())
        self.assertIsNotNone(amp.find('.//amp-analytics'))
        self.assertIsNotNone(amp.find('.//amp-analytics/script'))
        self.assertEqual(
            amp.find('*//amp-analytics/script').attrib['type'], 'application/json')
        self.assertIsNone(amp.find('*//amp-analytics/script').text)

        amp_analytics = IAMPSettings.__identifier__ + '.amp_analytics'
        api.portal.set_registry_record(amp_analytics, u'"foo": "bar"')
        amp = etree.HTML(self.view())
        self.assertEqual(
            amp.find('*//amp-analytics/script').text, u'"foo": "bar"')


class HelperViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_render(self):
        # define a publisher logo
        filename = 'logo-plone-ok.png'
        logo = load_b64encoded_image(filename)
        api.portal.set_registry_record(
            IAMPSettings.__identifier__ + '.publisher_logo', logo)

        # the view is registered in the context of the portal
        view = api.content.get_view(
            name='amp-publisher-logo', context=self.portal, request=self.request)

        # the publisher logo is rendered the we call the view
        rendered = view()
        headers = self.request.RESPONSE.headers
        self.assertEqual(headers['content-length'], '2257')
        self.assertEqual(headers['content-type'], 'image/png')
        self.assertEqual(
            headers['content-disposition'],
            "attachment; filename*=UTF-8''logo-plone-ok.png",
        )
        self.assertTrue(rendered.startswith('\x89PNG'))
