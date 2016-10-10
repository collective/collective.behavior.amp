# -*- coding: utf-8 -*-
"""Utility to transform HTML into AMP HTML.

See: https://www.ampproject.org/docs/reference/spec.html
"""
from collective.behavior.amp.config import AMP_INVALID_ELEMENTS
from collective.behavior.amp.logger import logger
from lxml import html
from plone.app.uuid.utils import uuidToObject
from Products.CMFPlone.utils import safe_unicode


class Html2Amp:

    """Utility to transform HTML into AMP HTML."""

    def remove_attribute(self, tag, attribute):
        """Remove attribute from tag."""
        try:
            del tag.attrib[attribute]
        except KeyError:
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

            try:
                # src="resolveuid/979bede6b93e46d386be493d852ed744"
                uuid = tag.attrib['src'].split('/')[1]
            except KeyError:
                # FIXME: the image has no src attribute; we should log
                #        an error message referencing the context
                # https://github.com/collective/collective.behavior.amp/issues/30
                continue
            except IndexError:
                # FIXME: what we should do if the <img> tag references
                #        an external resource?
                # https://github.com/collective/collective.behavior.amp/issues/29
                continue

            obj = uuidToObject(uuid)
            if obj is None:
                continue

            tag.attrib['src'] = obj.absolute_url()
            if obj.Description():
                tag.attrib['alt'] = safe_unicode(obj.Description())
            try:  # Dexterity
                width, height = obj.image.getImageSize()
            except AttributeError:  # Archetypes
                width, height = obj.getSize()
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

    def remove_invalid_attributes(self, el):
        """Remove AMP HTML invalid attributes.
        :param el: [required] LXML element to be sanitized.
        :type el: lxml.html.HtmlElement
        """
        for tag in el.iterdescendants():
            for key in tag.attrib.keys():
                remove = False
                if key.startswith('on') and key != 'on':
                    remove = True
                elif key == 'style':
                    remove = True
                elif key == 'xmlns' or key.startswith('xml:'):
                    remove = True
                if remove:
                    del tag.attrib[key]
                    logger.debug(
                        '"{0}" attribute was removed from tag <{1}>'.format(key, tag.tag))

    def __call__(self, code):
        el = html.fromstring(code.decode('utf-8'))

        # by default our RichText generates a list of <p> tags without parent
        # in this case lxml automatically add a <span> around these tags
        # here we change this parent tag into a <div class='amp-text'>
        el.tag = 'div'
        el.attrib['class'] = 'amp-text'

        self.transform_img_tags(el)
        self.remove_invalid_tags(el)
        self.remove_invalid_attributes(el)
        return html.tostring(el)
