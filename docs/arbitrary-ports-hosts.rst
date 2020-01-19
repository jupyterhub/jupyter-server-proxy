.. _arbitrary-ports:

==================================
Accessing Arbitrary Ports or Hosts
==================================

If you already have a server running on localhost listening on
a port, you can access it through the notebook at
``<notebook-base>/proxy/<port>``.
The URL will be rewritten to remove the above prefix.

You can disable URL rewriting by using
``<notebook-base>/proxy/absolute/<port>`` so your server will receive the full
URL in the request.

This works for all ports listening on the local machine.

You can also specify arbitrary hosts in order to proxy traffic from
another machine on the network ``<notebook-base>/proxy/<host>:<port>``.

For security reasons the host must match an entry in the whitelist in your configuration.

With JupyterHub
===============

Let's say you are using a JupyterHub set up on a remote machine,
and you have a process running on that machine listening on port
8080. If your hub URL is ``myhub.org``, each user can
access the service running on port 8080 with the URL
``myhub.org/hub/user-redirect/proxy/8080``. The ``user-redirect``
will make sure that:

#. It provides a redirect to the correct URL for the particular
   user who is logged in
#. If a user is not logged in, it'll present them with a login
   screen. They'll be redirected there after completing authentication.

You can also set ``c.Spawner.default_url`` to ``/proxy/8080`` to have
users be shown to your application directly after logging in -
without ever seeing the notebook interface.

Without JupyterHub
==================

A very similar set up works when you don't use JupyterHub. You
can construct the URL with ``<notebook-url>/proxy/<port>``.

If your notebook url is ``http://localhost:8888`` and you have
a process running listening on port 8080, you can access it with
the URL ``http://localhost:8888/proxy/8080``.

This is mostly useful for testing, since you can normally just
access services on your local machine directly.

From Notebook Extension
=======================

If you have a client side extension for the classic Jupyter Notebook
interface (nbextension), you can construct the URL for accessing
your service in this way:

.. code:: js

   define(['base/js/utils'], function(utils) {
     // Get base URL of current notebook server
     var base_url = utils.get_body_data('baseUrl');

     // Construct URL of our proxied service
     var service_url = base_url + 'proxy/' + port;

     // Do stuff with your service_url
   });

You can then make HTTP / Websocket requests as you wish from your
code.

From JupyterLab Extension
=========================

Accessing your service from a JupyterLab extension is similar to
accessing it from a classic notebook extension.

.. code:: typescript

   import { PageConfig } from '@jupyterlab/coreutils';

   // Get base URL of current notebook server
   let base_url = PageConfig.getBaseUrl()

   // Construct URL of our proxied service
   let service_url = base_url + 'proxy/' + port;

   // Do stuff with your service_url