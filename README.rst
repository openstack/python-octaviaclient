Team and repository tags
========================

.. image:: https://governance.openstack.org/tc/badges/python-octaviaclient.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on

python-octaviaclient
====================

Octavia client for OpenStack Load Balancing

This is an OpenStack Client (OSC) plugin for Octavia, an OpenStack
Load Balancing project.

For more information about Octavia see:
https://docs.openstack.org/octavia/latest/

For more information about the OpenStack Client see:
https://docs.openstack.org/python-openstackclient/latest/

* Free software: Apache license
* Documentation: https://docs.openstack.org/octavia/latest/
* Source: https://opendev.org/openstack/python-octaviaclient
* Release notes: https://docs.openstack.org/releasenotes/python-octaviaclient/
* Bugs: https://storyboard.openstack.org/#!/project/911

Getting Started
===============

.. note:: This is an OpenStack Client plugin. The ``python-openstackclient``
          project should be installed to use this plugin.

Octavia client can be installed from PyPI using pip::

    pip install python-octaviaclient

If you want to make changes to the Octavia client for testing and contribution,
make any changes and then run::

    python setup.py develop

or::

    pip install -e .
