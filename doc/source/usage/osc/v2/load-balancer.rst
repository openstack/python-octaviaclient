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

====
pool
====

loadbalancer pool list
----------------------

List pools

.. program:: loadbalancer pool list
.. code:: bash

    openstack loadbalancer pool list

loadbalancer pool show
----------------------

Show the details of a single pool

.. program:: loadbalancer pool show
.. code:: bash

    openstack loadbalancer pool show
        <pool>

.. _loadbalancer_pool_list-pool:
.. describe:: <pool>

    Name or UUID of the pool.

loadbalancer pool create
------------------------

Create a pool

.. program:: loadbalancer pool show
.. code:: bash

    openstack loadbalancer pool create
        [--name <name>]
        [--description <description>]
        --protocol {'TERMINATED_HTTPS','HTTP','HTTPS','TCP','PROXY'}
        [--listener <listener>]
        [--loadbalancer <load_balancer>]
        [--session-persistence <session persistence>]
        --lb-algorithm {'SOURCE_IP','ROUND_ROBIN','LEAST_CONNECTIONS'}
        [--project <project>]
        [--enable | --disable]

.. option:: --name <name>

    Set pool name.

.. option:: --description <description>

    Set pool description.

.. option:: --protocol {'TERMINATED_HTTPS','HTTP','HTTPS','TCP','PROXY'}

    Set the pool protocol.

.. option:: --listener <listener>

    Listener to add the pool to (name or ID).

.. option:: --loadbalancer <load_balancer>

    Load balancer to add the pool to (name or ID).

.. option:: --session-persistence <session persistence>

    Set the session persistence for the listener (key=value).

.. option:: --lb-algorithm {'SOURCE_IP','ROUND_ROBIN','LEAST_CONNECTIONS'}

    Load balancing algorithm to use.

.. option:: --project <project>

    Set the project owning this pool (name or ID).

.. option:: --enable

    Enable pool (default).

.. option:: --disable

    Disable pool.

loadbalancer pool set
---------------------

Update a pool

.. program:: loadbalancer pool set
.. code:: bash

    openstack loadbalancer pool set
        [--name <name>]
        [--description <description>]
        [--protocol {'TERMINATED_HTTPS','HTTP','HTTPS','TCP','PROXY'}]
        [--loadbalancer <load_balancer>]
        [--listener <listener>]
        [--session-persistence <session_persistence>]
        [--lb-algorithm {'SOURCE_IP','ROUND_ROBIN','LEAST_CONNECTIONS'}]
        [--enable | --disable]
        <pool>

.. option:: --name <name>

    Set the name of the pool.

.. option:: --description <description>

    Set the description of the pool.

.. option:: --protocol {'TERMINATED_HTTPS','HTTP','HTTPS','TCP','PROXY'}

    Set protocol for the pool.

.. option:: --loadbalancer <load_balancer>

    Load balncer to add the pool to (name or ID).

.. option:: --listener <listener>

    Listener to add the pool to (name or ID).

.. option:: --session-persistence <session_persistence>

    Set the session persistence for the listener (key=value).

.. option:: --lb-algorithm {'SOURCE_IP','ROUND_ROBIN','LEAST_CONNECTIONS'}

    Set the load balancing algorithm to use.

.. option:: --enable

    Enable pool.

.. option:: --disable

    Disable pool.

.. _loadbalancer_pool_set-pool:
.. describe:: <pool>

    Pool to update (name or ID).

loadbalancer pool delete
------------------------

Delete a pool

.. program:: loadbalancer pool delete
.. code:: bash

    openstack loadbalancer pool delete
        <pool>

.. _loadbalancer_pool_delete-pool:
.. describe:: <pool>

    Pool to delete (name or ID).

======
member
======

loadbalancer member list
------------------------

List members in a pool

.. program:: loadbalancer member list
.. code:: bash

    openstack loadbalancer member list
        <pool>

.. _loadbalancer_member_list-pool:
.. describe:: <pool>

   Pool name or ID to list the members of.

loadbalancer member show
------------------------

Shows details of a single Member

.. program:: loadbalancer member show
.. code:: bash

    openstack loadbalancer member show
        <pool>
        <member>

.. _loadbalancer_member_show-pool:
.. describe:: <pool>

   Pool name or ID to show the members of.

.. _loadbalancer_member_show-member:
.. describe:: <member>

   Name or ID of the member to show.

loadbalancer member create
--------------------------

Creating a member in a pool

.. program:: loadbalancer member create
.. code:: bash

    openstack loadbalancer member create
        [--name <name>]
        [--weight <weight>]
        --address <ip_address>
        [--subnet-id <subnet_id>]
        --protocol-port <protocol_port>
        [--monitor-port <monitor_port>]
        [--monitor-address <monitor_address>]
        [--enable | --disable]
        <pool>

.. option:: --name <name>

    Set the name of the member.

.. option:: --weight <weight>

    The weight of a member determines the portion of requests or connections it services compared to the other members of the pool.

.. option:: --address <ip_address>

    The IP address of the backend member server.

.. option:: --subnet-id <subnet_id>

    The subnet ID the member service is accessible from.

.. option:: --protocol-port <protocol_port>

    The protocol port number the backend member server is listening on.

.. option:: --monitor-port <monitor_port>

    An alternate protocol port used for health monitoring a backend member.

.. option:: --monitor-address <monitor_address>

    An alternate IP address used for health monitoring a backend member.

.. option:: --enable

    Enable member (default).

.. option:: --disable

    Disable member.

.. _loadbalancer_member_create-pool:
.. describe:: <pool>

    ID or name of the pool to create the member for.

loadbalancer member set
-----------------------

Update a member

.. program:: loadbalancer member set
.. code:: bash

    openstack loadbalancer member set
        [--name <name>]
        [--weight <weight>]
        [--address <ip_address>]
        [--subnet-id <subnet_id>]
        [--protocol-port <protocol_port>]
        [--monitor-port <monitor_port>]
        [--monitor-address <monitor_address>]
        [--enable | --disable]
        <pool>
        <member>

.. option:: --name <name>

    Set the name of the member.

.. option:: --weight <weight>

    Set the weight of member in the pool.

.. option:: --monitor-port <monitor_port>

    An alternate protocol port used for health monitoring a backend member.

.. option:: --monitor-address <monitor_address>

    An alternate IP address used for health monitoring a backend member.

.. option:: --enable

    Enable the member.

.. option:: --disable

    Disbale the member.

.. _loadbalancer_member_set-pool:
.. describe:: <pool>

    Pool that the member to update belongs to (name or ID).

.. _loadbalancer_member_set-member:
.. describe:: <member>

    Name or ID of the member to update.

loadbalancer member delete
--------------------------

Delete a member from a pool

.. program:: loadbalancer member delete
.. code:: bash

    openstack loadbalancer member delete
        <pool>
        <member>

.. _loadbalancer_member_delete-pool:
.. describe:: <pool>

    Pool name or ID to delete the member from.

.. _loadbalancer_member_delete-member:
.. describe:: <member>

    ID or name of the member to update.

========
l7policy
========

loadbalancer l7policy list
--------------------------

List l7policies

.. program:: loadbalancer l7policy delete
.. code:: bash

    openstack loadbalancer l7policy list

loadbalancer l7policy show
--------------------------

Show the details of a single l7policy

.. program:: loadbalancer l7policy delete
.. code:: bash

    openstack loadbalancer l7policy show
        <policy>

.. _loadbalancer_l7policy_show-policy:
.. describe:: <policy>

    Name or UUID of the l7policy.


loadbalancer l7policy create
----------------------------

Create a l7policy

.. program:: loadbalancer l7policy delete
.. code:: bash

    openstack loadbalancer l7policy create
        [--name <name>]
        [--description <description>]
        [--redirect-pool <pool>]
        --action {'REDIRECT_TO_URL','REDIRECT_TO_POOL','REJECT'}
        [--redirect-url <url>]
        [--project <project>]
        [--position <position>]
        [--enable | --disable]
        <listener>

.. option:: --name <name>

    Set the l7policy name.

.. option:: --description <description>

    Set l7policy description.

.. option:: --redirect-pool <pool>

    Set the pool to redirect requests to (name or ID).

.. option:: --action {'REDIRECT_TO_URL','REDIRECT_TO_POOL','REJECT'}

    Set the action of the policy.

.. option:: --redirect-url <url>

    Set the URL to redirect requests to.

.. option:: --position <position>

    Sequence number of this L7 Policy.

.. option:: --enable

    Enable l7policy (default).

.. option:: --disable

    Disable l7policy.

.. _loadbalancer_l7policy_create-listener:
.. describe:: <listener>

    Listener to add l7policy to (name or ID).

loadbalancer l7policy set
-------------------------

Update a l7policy

.. program:: loadbalancer l7policy set
.. code:: bash

    openstack loadbalancer l7policy set
        [--listener <listener>]
        [--name <name>]
        [--description <description>]
        [--redirect-pool <pool>]
        [--action {'REDIRECT_TO_URL','REDIRECT_TO_POOL','REJECT'}]
        [--redirect-url <url>]
        [--position <position>]
        [--enable | --disable]
        <policy>

.. option:: --name <name>

    Set l7policy name.

.. option:: --description <description>

    Set l7policy description.

.. option:: --redirect-pool <pool>

    Set the pool to redirect requests to (name or ID).

.. option:: --action {'REDIRECT_TO_URL','REDIRECT_TO_POOL','REJECT'}

    Set the action of the policy.

.. option:: --redirect-url <url>

    Set the URL to redirect requests to.

.. option:: --position <position>

    Set sequence number of this L7 Policy.

.. option:: --enable

    Enable l7policy.

.. option:: --disable

    Disable l7policy.

.. _loadbalancer_l7policy_set-policy:
.. describe:: <policy>

    L7policy to update (name or ID).

loadbalancer l7policy delete
----------------------------

Delete a l7policy

.. program:: loadbalancer l7policy delete
.. code:: bash

    openstack loadbalancer l7policy delete
        <policy>

.. _loadbalancer_l7policy_delete-policy:
.. describe:: <policy>

    L7policy to delete (name or ID).
