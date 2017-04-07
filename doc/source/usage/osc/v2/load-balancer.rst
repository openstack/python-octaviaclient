============
loadbalancer
============

loadbalancer list
-----------------

List load balancers

.. program:: loadbalancer list
.. code:: bash

    openstack loadbalancer list
        [--name <name>]
        [--enable | --disable]
        [--project <project-id>]

.. option:: --name <name>

    List load balancers according to their name.

.. option:: --enable

    List enabled load balancers.

.. option:: --disable

    List disabled load balancers.

.. option:: --project <project-id>

    List load balancers according to their project (name or ID).

loadbalancer show
-----------------

Show the details for a single load balancer

.. program:: loadbalancer show
.. code:: bash

    openstack loadbalancer show
        <loadbalancer>

.. _loadbalancer_show-loadbalancer:
.. describe:: <load_balancer>

    Name or UUID of the load balancer.

loadbalancer create
-------------------

Create a load balancer

.. program:: loadbalancer create
.. code:: bash

    openstack loadbalancer create
        [--name <name>]
        [--description <description>]
        [--vip-address <vip_address>]
        [--vip-port-id <vip_port_id>]
        [--vip-subnet-id <vip_subnet_id>]
        [--vip-network-id <vip_network_id>]
        [--project <project>]
        [--enable | --disable]

.. option:: --name <name>

    New load balancer name.

.. option:: --description <description>

    Set load balancer description.

.. option:: --vip-address <vip_address>

    Set the VIP IP Address.

.. option:: --vip-port-id <vip_port_id>

    Set Port for the load balancer (name or ID).

.. option:: --vip-subnet-id <vip_subnet_id>

    Set subnet for the load balancer (name or ID).

.. option:: --vip-network-id <vip_network_id>

    Set network for the load balancer (name or ID).

.. option:: --project <project>

    Project for the load balancer (name or ID).

.. option:: --enable

    Enable load balancer (default).

.. option:: --disable

    Disable load balancer.

loadbalancer set
----------------

Update a load balancer

.. program:: loadbalancer set
.. code:: bash

    openstack loadbalancer set
        [--enable | --disable]
        [--name <name>]
        [--description <description>]
        <load_balancer>

.. _loadbalancer_set-loadbalancer:
.. describe:: <load_balancer>

    Name or UUID of the load balancer to update.

.. option:: --enable

    Enable load balancer.

.. option:: --disable

    Disable load balancer.

.. option:: --name <name>

    Set load balancer name.

.. option:: --description <description>

    Set load balancer description.

loadbalancer delete
-------------------

Delete a load balancer

.. program:: loadbalancer delete
.. code:: bash

    openstack loadbalancer delete
        [--cascade]
        <load_balancer>

.. _loadbalancer_delete-loadbalancer:
.. describe:: <loadbalancer>

    Load balancers to delete (name or ID).

.. option:: --cascade

    Cascade the delete to all child elements of the load balancer.
