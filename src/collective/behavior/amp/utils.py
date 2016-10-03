# -*- coding: utf-8 -*-
from collective.behavior.amp.config import AMP_INVALID_ELEMENTS
from collective.behavior.amp.logger import logger
from lxml import html


class Html2Amp:
    def replace_tags(self, el):
        """Change <img> tags into <amp-img> tags with layout responsive.
        :param el: [required] LXML element to be sanitized.
        :type el: lxml.html.HtmlElement
        """
        for tag in el.xpath('//img'):
            tag.tag = 'amp-img'
            tag.attrib['layout'] = 'responsive'
            msg = '<img> tag was transformed into <amp-img>: {0}'
            logger.debug(msg.format(html.tostring(tag)))

    def remove_invalid_tags(self, el):
        """Remove invalid tags.
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

        self.replace_tags(el)
        self.remove_invalid_tags(el)
        return html.tostring(el)
