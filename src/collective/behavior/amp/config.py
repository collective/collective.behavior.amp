# -*- coding: utf-8 -*-
from plone import api

import pkg_resources


try:
    pkg_resources.get_distribution('sc.social.like')
except pkg_resources.DistributionNotFound:
    HAS_SOCIALLIKE = False
else:
    HAS_SOCIALLIKE = True

PROJECTNAME = 'collective.behavior.amp'

# https://github.com/ampproject/amphtml/blob/master/spec/amp-html-format.md
AMP_INVALID_ELEMENTS = [
    'base',
    'img',
    'video',
    'audio',
    'iframe',
    'frame',
    'frameset',
    'object',
    'param',
    'applet',
    'embed',
    'form',
    'input',
    'textarea',
    'select',
    'option',
    'style',  # valid just one tag style in the head
]

# https://github.com/ampproject/amphtml/blob/master/extensions/amp-analytics/amp-analytics.md
# TODO: we should provide a "Load example" button or something similar
AMP_ANALYTICS_DEFAULT = u"""
<amp-analytics type="googleanalytics" id="analytics1">
  <script type="application/json">
    {
      "vars": {
        "account": "UA-XXXXX-Y"
      },
      "triggers": {
        "trackPageview": {
          "on": "visible",
          "request": "pageview"
        }
      }
    }
  </script>
</amp-analytics>
"""

# https://github.com/ampproject/amphtml/blob/master/extensions/amp-social-share/amp-social-share.md
SOCIAL_SHARE_PROVIDERS = (
    'email',
    'facebook',
    'gplus',
    'linkedin',
    'pinterest',
    'twitter',
)

IS_PLONE_5 = api.env.plone_version().startswith('5')
