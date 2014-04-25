.. mediaphile documentation master file, created by
   sphinx-quickstart on Fri Apr 25 11:25:09 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to mediaphile's documentation!
======================================

Contents:

Here's some docs.

.. py:function:: send_message(sender, recipient, message_body, [priority=1])

   Send a message to a recipient

   :param str sender: The person sending the message
   :param str recipient: The recipient of the message
   :param str message_body: The body of the message
   :param priority: The priority of the message, can be a number 1-5
   :type priority: integer or None
   :return: the message id
   :rtype: int
   :raises ValueError: if the message_body exceeds 160 characters
   :raises TypeError: if the message_body is not a basestring

.. toctree::
   :maxdepth: 4

   introduction
   mediaphile

.. automodule:: mediaphile
.. automodule:: mediaphile.lib
.. automodule:: mediaphile.cli

.. autoclass:: mediaphile
    :members:

.. autoclass:: mediaphile.lib
    :members:

.. autoclass:: mediaphile.cli
    :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

