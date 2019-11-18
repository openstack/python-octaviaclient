Using Octavia CLI extensions to OpenStack Client
================================================

List of released CLI commands available in openstack client. These commands
can be referenced by doing ``openstack help loadbalancer``.

============
loadbalancer
============

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer create

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer delete

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer list

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer set

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer unset

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer show

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer stats show

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer status show

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer failover

========
listener
========

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer listener *

====
pool
====

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer pool *

======
member
======

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer member *

=============
healthmonitor
=============

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer healthmonitor *

========
l7policy
========

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer l7policy *

======
l7rule
======

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer l7rule *

=====
quota
=====

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer quota *

=======
amphora
=======

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer amphora *

========
provider
========

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer provider *

======
flavor
======

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer flavor *

=============
flavorprofile
=============

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer flavorprofile *

================
availabilityzone
================

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer availabilityzone *

=======================
availabilityzoneprofile
=======================

.. autoprogram-cliff:: openstack.load_balancer.v2
    :command: loadbalancer availabilityzoneprofile *
