.. image:: https://raw.githubusercontent.com/collective/collective.behavior.amp/master/docs/amp.png
    :align: left
    :alt: Accelerated Mobile Pages
    :height: 128px
    :width: 128px

*********************************************
Support for Accelerated Mobile Pages in Plone
*********************************************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

The `Accelerated Mobile Pages Project <https://www.ampproject.org/>`_ (AMP) is an open source project and service to accelerate content on mobile devices.

This package implements a behavior for Dexterity-based content types that adds an AMP HTML version of your content.
Most newest mobile browsers will serve this version by default.
Google will also link the mobile search results to this version.

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/collective.behavior.amp.svg
   :target: https://pypi.python.org/pypi/collective.behavior.amp

.. image:: https://img.shields.io/travis/collective/collective.behavior.amp/master.svg
    :target: http://travis-ci.org/collective/collective.behavior.amp

.. image:: https://img.shields.io/coveralls/collective/collective.behavior.amp/master.svg
    :target: https://coveralls.io/r/collective/collective.behavior.amp

Got an idea? Found a bug? Let us know by `opening a support ticket <https://github.com/collective/collective.behavior.amp/issues>`_.

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it:

.. code-block:: ini

    [buildout]
    ...
    eggs =
        collective.behavior.amp

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``Accelerated Mobile Pages Support`` and click the 'Activate' button.

Usage
-----

Go to 'Site Setup' and select 'Accelerated Mobile Pages';
set the publisher logo and the `AMP analytics code <https://developers.google.com/analytics/devguides/collection/amp-analytics/>`_, if available.

.. figure:: https://raw.githubusercontent.com/collective/collective.behavior.amp/master/docs/controlpanel.png
    :align: center
    :height: 720px
    :width: 768px

    The Accelerated Mobile Pages control panel configlet.

Go to 'Site Setup' and select 'Dexterity Content Types' and enable the 'Accelerated Mobile Pages' in your content types.
A new view named ``@@amp`` will become available in all instances of your content type.
The view will display the logo of your site, a global navigation sidebar, and the main fields of your content type (including title, byline, resume, body text, and related items, if available);
it will also include metadata as structured data.

If  `sc.social.like <https://pypi.python.org/pypi/sc.social.like>`_ is installed,
a list of social share buttons honoring the configured plugins will be displayed between the byline and the resume.
Note that you have to enter a valid Facebook ``app_id`` if you want to enable the Facebook button.

How does it work
----------------

AMP is a way to build web pages for static content that render fast.
AMP consists of three different parts:

AMP HTML
    AMP HTML is HTML with some restrictions for reliable performance and some extensions for building rich content beyond basic HTML.
AMP JS
    The AMP JS library ensures the fast rendering of AMP HTML pages.
Google AMP Cache
    The Google AMP Cache can be used to serve cached AMP HTML pages.

This package adds an alternate view to display your content as AMP HTML page,
and adds a link to it in the header of any other view:

.. code-block:: xml

  <link rel="amphtml" href="${context/absolute_url}/@@amp">

The body text is processed to remove invalid elements or to replace them by the corresponding AMP components.
