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


========
listener
========

loadbalancer listener list
--------------------------

List listeners

.. program:: loadbalancer listener list
.. code:: bash

    openstack loadbalancer listener list
        [--name <name>]
        [--enable | --disable]
        [--project <project>]

.. option:: --name <name>

    List listeners by listener name.

.. option:: --enable

    List enabled listeners.

.. option:: --disable

    List disabled listeners.

.. option:: --project <project>

    List listeners by project ID.

loadbalancer listener show
--------------------------

Show the details of a single listener

.. program:: loadbalancer listener show
.. code:: bash

    openstack loadbalancer listener show
        <listener>

.. _loadbalancer_listener_show-listener:
.. describe:: <listener>

    Name or UUID of the listener

loadbalancer listener create
----------------------------

Create a listener

.. program:: loadbalancer listener create
.. code:: bash

    openstack loadbalancer listener create
        [--description <description>]
        --protocol <protocol>
        [--connection-limit <limit>]
        [--default-pool <pool>]
        [--default-tls-container-ref <container-ref>]
        [--sni-container-refs [<container-ref> [<container-ref> ...]]]
        [--insert-headers <header=value,...>]
        --protocol-port <port>
        [--enable | --disable]
        <loadbalancer_id>

.. option:: --name <name>

    Set listener name.

.. option:: --description <description>

    Set the description of this listener.

.. option:: --protocol <protocol>

    The protocol for the listener

.. option:: --connection-limit <limit>

    The maximum number of connections permitted for this listener.

.. option:: --default-pool <pool>

    The name or ID of the pool used by the listener if no L7 policies match.

.. option:: --default-tls-container-ref <container-ref>

    The URI to the key manager service secrets container containing the certificate and key for TERMINATED_TLS listeners.

.. option:: --sni-container-refs [<container-ref> [<container-ref> ...]]

    A list of URIs to the key manager service secrets containers containing the certificates and keys for TERMINATED_TLS the listener using Server Name Indication.

.. option:: --insert-headers <header=value,...>

    A dictionary of optional headers to insert into the request before it is sent to the backend member.

.. option:: --protocol-port <port>

    Set the protocol port number for the listener.

.. option:: --enable

    Enable listener (default).

.. option:: --disable

    Disable listener.

loadbalancer listener set
-------------------------

Update a listener

.. program:: loadbalancer listener set
.. code:: bash

    openstack loadbalancer listener set
        [--name <name>]
        [--description <description>]
        [--protocol <protocol>]
        [--connection-limit <limit>]
        [--default-pool <pool-id>]
        [--default-tls-container-ref <container-ref>]
        [---sni-container-refs [<container-ref> [<container-ref> ...]]]
        [--insert-headers <header=value>]
        [--enable | --disable]
        <listener-id>

.. _loadbalancer_listener_set-listener:
.. describe:: <listener-id>

    Listener to modify (name or ID).

.. option:: --name <name>

    Set listener name.

.. option:: --description <description>

    Set the description of this listener.

.. option:: --connection-limit <limit>

    The maximum number of connections permitted for this listener.
    Default value is -1 which represents infinite connections.

.. option:: --default-pool <pool-id>

    The ID of the pool used by the listener if no L7 policies match.

.. option:: --default-tls-container-ref <container-ref>

    The URI to the key manager service secrets container containing the certificate and key for TERMINATED_TLS listeners.

.. option:: ---sni-container-refs [<container-ref> [<container-ref> ...]]

    A list of URIs to the key manager service secrets containers containing the certificates and keys for TERMINATED_TLS the listener using Server Name Indication.

.. option:: --insert-headers <header=value>

    A dictionary of optional headers to insert into the request before it is sent to the backend member.

.. option:: --enable

    Enable listener.

.. option:: --disable

    Disable listener.

loadbalancer listener delete
----------------------------

Delete a listener

.. program:: loadbalancer listener delete
.. code:: bash

    openstack loadbalancer listener delete
        <listener>

.. _loadbalancer_listener_delete-listener:
.. describe:: <listener>

    Listener to delete (name or ID).
