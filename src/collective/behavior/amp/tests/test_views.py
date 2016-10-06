# -*- coding: utf-8 -*-
from collective.behavior.amp.config import HAS_SOCIALLIKE
from collective.behavior.amp.interfaces import IAMPSettings
from collective.behavior.amp.testing import INTEGRATION_TESTING
from collective.behavior.amp.tests.utils import enable_amp_behavior
from collective.behavior.amp.tests.utils import get_file
from collective.behavior.amp.tests.utils import get_file_b64encoded
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

    def test_caching_headers(self):
        from App.Common import rfc1123_date
        self.view()
        headers = self.request.RESPONSE.headers
        self.assertEqual(headers['cache-control'], 'public')
        self.assertEqual(
            headers['last-modified'], rfc1123_date(self.newsitem.modified()))

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

    def _set_publisher_logo(self, filename):
        logo = get_file_b64encoded(filename)
        api.portal.set_registry_record(
            IAMPSettings.__identifier__ + '.publisher_logo', logo)

    def test_metadata_logo(self):
        # publisher logo information must be available if logo is loaded
        filename = 'logo-plone-ok.png'
        self._set_publisher_logo(filename)
        amp = etree.HTML(self.view())
        metadata = self._get_metadata_as_json(amp)
        self.assertIn('logo', metadata['publisher'])

        metadata = metadata['publisher']['logo']  # shortcut
        self.assertEqual(metadata['@type'], u'ImageObject')
        url = u'http://nohost/plone/@@amp-publisher-logo/{0}'.format(filename)
        self.assertEqual(metadata['url'], url)
        self.assertEqual(metadata['width'], 231)
        self.assertEqual(metadata['height'], 60)

    def test_logo(self):
        filename = 'logo-plone-ok.png'
        self._set_publisher_logo(filename)
        amp = etree.HTML(self.view())
        logo = amp.find('.//amp-img[@class="logo"]')
        self.assertIsNotNone(logo)
        url = u'http://nohost/plone/@@amp-publisher-logo/{0}'.format(filename)
        self.assertEqual(logo.attrib['src'], url)
        self.assertEqual(logo.attrib['alt'], 'Plone site')
        self.assertEqual(logo.attrib['width'], '231')
        self.assertEqual(logo.attrib['height'], '60')

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

    @unittest.skipIf(HAS_SOCIALLIKE, 'sc.social.like must not be installed')
    def test_no_amp_social_share(self):
        amp = etree.HTML(self.view())
        amp.findall('.//amp-social-share')
        self.assertEqual(len(amp.findall('.//amp-social-share')), 0)

    @unittest.skipUnless(HAS_SOCIALLIKE, 'sc.social.like must be installed')
    def test_amp_social_share(self):
        from sc.social.like.interfaces import ISocialLikeSettings
        # configure Facebook app_id before rendering
        app_id = ISocialLikeSettings.__identifier__ + '.facebook_app_id'
        api.portal.set_registry_record(app_id, '1234567890')

        amp = etree.HTML(self.view())
        amp.findall('.//amp-social-share')
        # Facebook and Twitter are enabled by default
        self.assertEqual(len(amp.findall('.//amp-social-share')), 2)
        # Facebook button is present and has data-param-app_id attribute
        facebook = amp.find('.//amp-social-share[@type="facebook"]')
        self.assertIsNotNone(facebook)
        self.assertEqual(facebook.attrib['data-param-app_id'], '1234567890')
        # Twitter button is present
        self.assertIsNotNone(
            amp.find('.//amp-social-share[@type="twitter"]'))

    def test_no_lead_image(self):
        enable_amp_behavior('Document')
        with api.env.adopt_roles(['Manager']):
            page = api.content.create(
                container=self.portal, type='Document', title='foo')
        view = api.content.get_view(
            name='amp', context=page, request=self.request)
        amp = etree.HTML(view())
        self.assertIsNone(amp.find('.//figure'))
        # no lead image information in metadata
        metadata = self._get_metadata_as_json(amp)
        self.assertNotIn('image', metadata)

    def test_lead_image_not_set(self):
        amp = etree.HTML(self.view())
        self.assertIsNone(amp.find('.//figure'))

    def test_lead_image(self):
        from plone.namedfile.file import NamedBlobImage
        filename = u'logo-plone-ok.png'
        self.newsitem.image = NamedBlobImage(
            data=get_file(filename), filename=filename)
        self.newsitem.image_caption = u'Mais amor, por favor!'
        amp = etree.HTML(self.view())
        lead_image = amp.find('.//figure/amp-img')
        self.assertIsNotNone(lead_image)
        self.assertTrue(lead_image.attrib['src'].endswith(filename))
        self.assertEqual(lead_image.attrib['layout'], 'responsive')
        self.assertEqual(lead_image.attrib['width'], '231')
        self.assertEqual(lead_image.attrib['height'], '60')
        self.assertEqual(
            amp.find('.//figure/figcaption').text, 'Mais amor, por favor!')

        # lead image information in metadata
        metadata = self._get_metadata_as_json(amp)
        self.assertIn('image', metadata)
        metadata = metadata['image']  # shortcut
        self.assertEqual(metadata['@type'], u'ImageObject')
        url = u'lorem-ipsum/@@download/image/{0}'.format(filename)
        self.assertTrue(metadata['url'].endswith(url))
        self.assertEqual(metadata['width'], 231)
        self.assertEqual(metadata['height'], 60)

    def test_no_amp_analytics(self):
        amp = etree.HTML(self.view())
        self.assertIsNone(amp.find('.//amp-analytics'))

    def test_amp_analytics(self):
        amp_analytics = IAMPSettings.__identifier__ + '.amp_analytics'
        api.portal.set_registry_record(amp_analytics, u'"foo": "bar"')
        amp = etree.HTML(self.view())
        analytics = amp.find('.//amp-analytics/script')
        self.assertIsNotNone(analytics)
        self.assertEqual(analytics.attrib['type'], u'application/json')
        self.assertEqual(analytics.text, u'"foo": "bar"')

    def test_no_related_items(self):
        amp = etree.HTML(self.view())
        self.assertIsNone(amp.find('.//div[@class="amp-related"]'))

    def test_related_items(self):
        from z3c.relationfield import RelationValue
        from zope.component import getUtility
        from zope.intid.interfaces import IIntIds
        with api.env.adopt_roles(['Manager']):
            r1 = api.content.create(
                container=self.portal, type='News Item', title='foo')
            r2 = api.content.create(
                container=self.portal, type='Image', title='bar')

        intids = getUtility(IIntIds)
        self.newsitem.relatedItems = [
            RelationValue(intids.getId(r1)), RelationValue(intids.getId(r2))]

        amp = etree.HTML(self.view())
        relations = amp.findall('.//div[@class="amp-related"]//a')
        self.assertEqual(len(relations), 2)
        self.assertEqual(relations[0].text, 'foo')
        self.assertTrue(relations[0].attrib['href'].endswith('foo'))
        self.assertEqual(relations[1].text, 'bar')
        self.assertTrue(relations[1].attrib['href'].endswith('bar/view'))


class HelperViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_render(self):
        # define a publisher logo
        filename = 'logo-plone-ok.png'
        logo = get_file_b64encoded(filename)
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
