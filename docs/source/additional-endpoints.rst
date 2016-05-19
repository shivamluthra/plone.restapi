=================================
Additional Endpoints (MOCKS ONLY)
=================================

These are mocked endpoints for use during the Barcelona 2016 Sprint.

.. meta::
   :robots: noindex, nofollow

.. warning::
   These endpoints simply deliver mocked content (canned responses). They are
   not intended for actual use, but instead serve as a skeleton to flesh out
   different aspects of the API during the Barcelona 2016 sprint.

Theme
========

Requesting for overridden resources
-----------------------------------

.. code::

  GET /:portal/@theme HTTP/1.1
  Host: localhost:8080
  Accept: application/json

Example:

.. literalinclude:: _json/theme.json
   :language: js


Components
==========

Get the required component(s)
------------------------------

.. code::

 GET /:portal/@components/:[id,] HTTP/1.1
 Host: localhost:8080
 Accept: application/json

Examples:

.. literalinclude:: _json/components_navigation.json
  :language: js


.. literalinclude:: _json/components_breadcrumbs.json
  :language: js


Actions
=======

Get the available actions for the given context
-----------------------------------------------

.. code::

 GET /:path/@actions HTTP/1.1
 Host: localhost:8080
 Accept: application/json

Example:

.. literalinclude:: _json/actions.json
  :language: js


Framed Responses
================

.. code::

 GET /:path?frame=object HTTP/1.1
 Host: localhost:8080
 Accept: application/json

Example:

.. literalinclude:: _json/frame_object.json
  :language: js


Authentication
==============

Login
-----

.. code::

 POST /:path/@login HTTP/1.1
 Host: localhost:8080
 Accept: application/json

Example:

.. literalinclude:: _json/login.json
  :language: js
