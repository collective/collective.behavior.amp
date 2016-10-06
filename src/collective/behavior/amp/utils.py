# -*- coding: utf-8 -*-
from collective.behavior.amp.config import AMP_INVALID_ELEMENTS
from collective.behavior.amp.logger import logger
from lxml import html
from plone.app.uuid.utils import uuidToObject


class Html2Amp:

    """Utility to transform HTML into AMP HTML."""

    def remove_attribute(self, tag, attribute):
        """Remove attribute from tag."""
        try:
            del tag.attrib[attribute]
        except AttributeError:
            pass

    def transform_img_tags(self, el):
        """Transform <img> tags into <amp-img> tags.
        :param el: [required] LXML element to be transformed.
        :type el: lxml.html.HtmlElement
        """
        # AMP HTML images are described using the "amp-img" tag
        # they should include: src, width, height and alt attributes only
        for tag in el.xpath('//img'):
            tag.tag = 'amp-img'
            # src="resolveuid/979bede6b93e46d386be493d852ed744"
            uuid = tag.attrib['src'].split('/')[1]
            obj = uuidToObject(uuid)
            if obj is None:
                continue
            tag.attrib['src'] = obj.absolute_url()
            if obj.Description():
                tag.attrib['alt'] = obj.Description()
            width, height = obj.image.getImageSize()
            tag.attrib['width'] = unicode(width)
            tag.attrib['height'] = unicode(height)
            tag.attrib['layout'] = 'responsive'
            self.remove_attribute(tag, 'class')  # should not include class
            msg = '<img> tag was transformed into <amp-img>: {0}'
            logger.debug(msg.format(html.tostring(tag)))

    def remove_invalid_tags(self, el):
        """Remove AMP HTML invalid elements.
        :param el: [required] LXML element to be sanitized.
        :type el: lxml.html.HtmlElement
        """
        for tag in el.iterdescendants():
            if tag.tag not in AMP_INVALID_ELEMENTS:
                continue
            parent = tag.getparent()
            parent.remove(tag)
            logger.debug('<{0}> tag was removed'.format(tag.tag))

    def __call__(self, code):
        el = html.fromstring(code)

        # by default our RichText generates a list of <p> tags without parent
        # in this case lxml automatically add a <span> around these tags
        # here we change this parent tag into a <div class='amp-text'>
        el.tag = 'div'
        el.attrib['class'] = 'amp-text'

        self.transform_img_tags(el)
        self.remove_invalid_tags(el)
        return html.tostring(el)
