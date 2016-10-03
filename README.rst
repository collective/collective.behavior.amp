.. image:: https://raw.githubusercontent.com/collective/collective.behavior.amp/master/docs/amp.png
    :align: left
    :alt: Accelerated Mobile Pages
    :height: 100px
    :width: 100px

*********************************************
Support for Accelerated Mobile Pages in Plone
*********************************************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

collective.behavior.amp implements a behavior for Dexterity-based content types that creates an AMP (Accelerated Mobile Pages) version of your content.

collective.behavior.amp is based on Google AMP projetc principles and recomendations, visit the project page to know more: https://www.ampproject.org

How this package works?
-----------------------

collective.behavior.amp creates an alternate and very light template for your content, and adds a link in the header of your regular template to the AMP version. 
To manually visit the AMP version just add /amp to your content URL. Most newest mobile browsers will serve this version by default. Google also will link the mobile search results to this version.

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/collective.behavior.amp.svg
   :target: https://pypi.python.org/pypi/collective.behavior.amp

.. image:: https://img.shields.io/travis/collective/collective.behavior.amp/master.svg
    :target: http://travis-ci.org/collective/collective.behavior.amp

.. image:: https://img.shields.io/coveralls/collective/collective.behavior.amp/master.svg
    :target: https://coveralls.io/r/collective/collective.behavior.amp

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/collective.behavior.amp/issues

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

Check the box next to ``collective.behavior.amp`` and click the 'Activate' button.

Usage
-----

If  `sc.social.like <https://pypi.python.org/pypi/sc.social.like>`_ is installed,
``collective.behavior.amp`` will display a list of social share buttons honoring the configured plugins.
Note that you have to enter a valid Facebook ``app_id`` if you want to enable the Facebook button.
