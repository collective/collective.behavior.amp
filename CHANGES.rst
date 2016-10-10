Changelog
=========

There's a frood who really knows where his towel is.

1.0a3 (unreleased)
------------------

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

- Fix exception on ``AMPView`` when content has no lead image.
  [hvelarde]


1.0a1 (2016-10-06)
------------------

- Initial release.

.. _`#26`: https://github.com/collective/collective.behavior.amp/issues/26
