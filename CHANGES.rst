Changelog
=========

There's a frood who really knows where his towel is.

1.0a4 (unreleased)
------------------

- Add support for WhatsApp in ``<amp-social-share>`` tag.
  [hvelarde]


1.0a3 (2017-04-13)
------------------

- Fix i18n and update Brazilian Portuguese and Spanish translations (fixes `#44`_).
  [hvelarde]

- Set correct language information (fixes `#43`_).
  [hvelarde]

- Add support for the ``amp-sticky-ad`` tag.
  [hvelarde]

- Fix support for the ``<amp-analytics>`` tag.
  [agnogueira, hvelarde]

- Fix CSS error in logo position.
  [kakshay21]

- Avoid exception when related items relation is broken.
  [rodfersou]

- Fix loading order for main AMP script.
  [hvelarde]

- Add class for social icon <div> tag.
  [agnogueira]

- Move description to article header.
  [agnogueira]

- Do not fail if an image doesn't have a ``src`` attribute,
  or if it was referenced inside the body text as an external resource.
  [hvelarde]

- Clean up invalid AMP HTML attributes (fixes `#26`_).
  [rodfersou]

- Explicitly disable any Diazo theme on the AMP HTML view.
  [hvelarde]

- Use ``byline`` field (if present) to get the name of the content's author.
  [hvelarde]

- Fix various exceptions raised when content has Archetypes based lead images.
  [hvelarde]

1.0a2 (2016-10-06)
------------------

- Fix exception on the AMP HTML view when content has no lead image.
  [hvelarde]


1.0a1 (2016-10-06)
------------------

- Initial release.

.. _`#26`: https://github.com/collective/collective.behavior.amp/issues/26
.. _`#43`: https://github.com/collective/collective.behavior.amp/issues/43
.. _`#44`: https://github.com/collective/collective.behavior.amp/issues/44
