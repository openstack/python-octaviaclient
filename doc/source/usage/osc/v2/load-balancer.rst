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
        --protocol {TCP,HTTP,HTTPS,TERMINATED_HTTPS}
        [--connection-limit <limit>]
        [--default-pool <pool>]
        [--default-tls-container-ref <container-ref>]
        [--sni-container-refs [<container-ref> [<container-ref> ...]]]
        [--insert-headers <header=value,...>]
        --protocol-port <port>
        [--enable | --disable]
        <load_balancer>

.. option:: --name <name>

    Set listener name.

.. option:: --description <description>

    Set the description of this listener.

.. option:: --protocol {TCP,HTTP,HTTPS,TERMINATED_HTTPS}

    The protocol for the listener.

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

.. _loadbalancer_listener_create-loadbalancer:
.. describe:: <load_balancer>

    Load balancer for the listener (name or ID).

loadbalancer listener set
-------------------------

Update a listener

.. program:: loadbalancer listener set
.. code:: bash

    openstack loadbalancer listener set
        [--name <name>]
        [--description <description>]
        [--connection-limit <limit>]
        [--default-pool <pool>]
        [--default-tls-container-ref <container-ref>]
        [---sni-container-refs [<container-ref> [<container-ref> ...]]]
        [--insert-headers <header=value>]
        [--enable | --disable]
        <listener>

.. _loadbalancer_listener_set-listener:
.. describe:: <listener>

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
        --protocol {TCP,HTTP,HTTPS,TERMINATED_HTTPS,PROXY}
        [--listener <listener>]
        [--loadbalancer <load_balancer>]
        [--session-persistence <session persistence>]
        --lb-algorithm {SOURCE_IP,ROUND_ROBIN,LEAST_CONNECTIONS}
        [--project <project>]
        [--enable | --disable]

.. option:: --name <name>

    Set pool name.

.. option:: --description <description>

    Set pool description.

.. option:: --protocol {TCP,HTTP,HTTPS,TERMINATED_HTTPS,PROXY}

    Set the pool protocol.

.. option:: --listener <listener>

    Listener to add the pool to (name or ID).

.. option:: --loadbalancer <load_balancer>

    Load balancer to add the pool to (name or ID).

.. option:: --session-persistence <session persistence>

    Set the session persistence for the listener (key=value).

.. option:: --lb-algorithm {SOURCE_IP,ROUND_ROBIN,LEAST_CONNECTIONS}

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
        [--protocol {TCP,HTTP,HTTPS,TERMINATED_HTTPS,PROXY}]
        [--loadbalancer <load_balancer>]
        [--listener <listener>]
        [--session-persistence <session_persistence>]
        [--lb-algorithm {SOURCE_IP,ROUND_ROBIN,LEAST_CONNECTIONS}]
        [--enable | --disable]
        <pool>

.. option:: --name <name>

    Set the name of the pool.

.. option:: --description <description>

    Set the description of the pool.

.. option:: --protocol {TCP,HTTP,HTTPS,TERMINATED_HTTPS,PROXY}

    Set protocol for the pool.

.. option:: --loadbalancer <load_balancer>

    Load balncer to add the pool to (name or ID).

.. option:: --listener <listener>

    Listener to add the pool to (name or ID).

.. option:: --session-persistence <session_persistence>

    Set the session persistence for the listener (key=value).

.. option:: --lb-algorithm {SOURCE_IP,ROUND_ROBIN,LEAST_CONNECTIONS}

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
        --action {REDIRECT_TO_URL,REDIRECT_TO_POOL,REJECT}
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

.. option:: --action {REDIRECT_TO_URL,REDIRECT_TO_POOL,REJECT}

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
        [--action {REDIRECT_TO_URL,REDIRECT_TO_POOL,REJECT}]
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

.. option:: --action {REDIRECT_TO_URL,REDIRECT_TO_POOL,REJECT}

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

======
l7rule
======

loadbalancer l7rule list
------------------------

List l7rules for l7policy

.. program:: loadbalancer l7rule list
.. code:: bash

    openstack loadbalancer l7rule list
        --l7policy <l7policy>

.. _loadbalancer_l7rule_list-l7policy:
.. describe:: <l7policy>

    l7policy to list rules for (name or ID).

loadbalancer l7rule show
------------------------

Show the details of a single l7rule

.. program:: loadbalancer l7rule show
.. code:: bash

    openstack loadbalancer l7rule show
        <l7policy>
        <rule-id>

.. _loadbalancer_l7rule_show-l7policy:
.. describe:: <l7policy>

    l7policy to show rule from (name or ID)

.. _loadbalancer_l7rule_show-rule-id:
.. describe:: <l7rule_id>

    l7rule to show

loadbalancer l7rule create
--------------------------

Create a l7rule

.. program:: loadbalancer l7rule create
.. code:: bash

    openstack loadbalancer l7rule create
        --compare-type {REGEX,EQUAL_TO,CONTAINS,ENDS_WITH,STARTS_WITH}
        [--invert]
        --value <value>
        [--key <key>]
        [--project <project>]
        --type {FILE_TYPE,PATH,COOKIE,HOST_NAME,HEADER}
        [--enable | --disable]
        <l7policy>

.. option:: --compare-type {REGEX,EQUAL_TO,CONTAINS,ENDS_WITH,STARTS_WITH}

    Set the compare type for the l7rule.

.. option:: --invert

    Invert l7rule.

.. option:: --value <value>

    Set the rule value to match on.

.. option:: --key <key>

    Set the key for the l7rule's value to match on.

.. option:: --project <project>

    Project for the l7rule (name or ID).

.. option:: --type {FILE_TYPE,PATH,COOKIE,HOST_NAME,HEADER}

    Set the type for the l7rule.

.. option:: --enable

    Enable l7rule (default).

.. option:: --disable

    Disable l7rule.

.. _loadbalancer_l7rule_create-l7policy:
.. describe:: <l7policy>

    l7policy to add l7rule to (name or ID).


loadbalancer l7rule set
-----------------------

Update a l7rule

.. program:: loadbalancer l7rule set
.. code:: bash

    openstack loadbalancer l7rule set
        [--compare-type {REGEX,EQUAL_TO,CONTAINS,ENDS_WITH,STARTS_WITH}]
        [--invert]
        [--value <value>]
        [--key <key>]
        [--type {FILE_TYPE,PATH,COOKIE,HOST_NAME,HEADER}]
        [--enable | --disable]
        --l7policy <policy>
        <l7rule_id>

.. option:: --compare-type {REGEX,EQUAL_TO,CONTAINS,ENDS_WITH,STARTS_WITH}

    Set the compare type for the l7rule.

.. option:: --invert

    Invert l7rule.

.. option:: --value <value>

    Set the rule value to match on.

.. option:: --key <key>

    Set the key for the l7rule's value to match on.

.. option:: --type {FILE_TYPE,PATH,COOKIE,HOST_NAME,HEADER}

    Set the type for the l7rule.

.. option:: --enable

    Enable l7rule.

.. option:: --disable

    Disable l7rule.

.. _loadbalancer_l7rule_set-l7policy:
.. describe:: <l7policy>

    L7policy to update l7rule on (name or ID)

.. _loadbalancer_l7rule_set-l7rule_id:
.. describe:: <l7rule_id>

    l7rule to update

loadbalancer l7rule delete
--------------------------

.. program:: loadbalancer l7rule delete
.. code:: bash

    openstack loadbalancer l7rule delete
        <l7policy>
        <rule_id>

.. _loadbalancer_l7rule_delete-l7policy:
.. describe:: <l7policy>

    l7policy to delete rule from (name or ID).

.. _loadbalancer_l7rule_delete-l7rule_id:
.. describe:: <l7rule_id>

    l7rule to delete.

=============
healthmonitor
=============

loadbalancer healthmonitor list
-------------------------------

List health monitors

.. program:: loadbalancer healthmonitor list
.. code:: bash

    openstack loadbalancer healthmonitor list

loadbalancer healthmonitor show
-------------------------------

Show the details of a single health monitor

.. program:: loadbalancer healthmonitor show
.. code:: bash

    openstack loadbalancer healthmonitor show
        <health_monitor>

.. _loadbalancer_healthmonitor_show-health_monitor:
.. describe:: <health_monitor>

    Name or UUID of the health monitor.

loadbalancer healthmonitor create
---------------------------------

Create a health monitor

.. program:: loadbalancer healthmonitor create
.. code:: bash

    openstack loadbalancer healthmonitor create
        [--name <name>]
        --delay <delay>
        [--expected-codes <codes>]
        [--http_method {GET,POST,DELETE,PUT,HEAD,OPTIONS,PATCH,CONNECT,TRACE}]
        --timeout <timeout>
        --max-retries <max_retries>
        [--url-path <url_path>]
        --type {PING,HTTP,TCP,HTTPS}
        [--max-retries-down <max_retries_down>]
        [--project <project>]
        [--enable | --disable]
        <pool>

.. option:: --name <name>

    Set the health monitor name.

.. option:: --delay <delay>

    Set the time in seconds, between sending probes to members.

.. option:: --expected-codes <codes>

    Set the list of HTTP status codes expected in response from the member to declare it healthy.

.. option:: --http_method {GET,POST,DELETE,PUT,HEAD,OPTIONS,PATCH,CONNECT,TRACE}

    Set the HTTP method that the health monitor uses for requests.

.. option:: --timeout <timeout>

    Set the maximum time, in seconds, that a monitor waits to connect before it times out.
    This value must be less than the delay value.

.. option:: --max-retries <max_retries>

    The number of successful checks before changing the operating status of the member to ONLINE.

.. option:: --url-path <url_path>

    Set the HTTP URL path of the request sent by the monitor to test the health of a backend member.

.. option:: --type {PING,HTTP,TCP,HTTPS}

    Set the type of health monitor.

.. option:: --max-retries-down <max_retries_down>

    Set the number of allowed check failures before changing the operating status of the member to ERROR.

.. option:: --project <project>

    Project to use for the health monitor (name or ID).

.. option:: --enable

    Enable health monitor (default).

.. option:: --disable

    Disable health monitor.

.. _loadbalancer_healthmonitor_create-pool_id:
.. describe:: <pool>

    Set the pool for the health monitor (name or ID).

loadbalancer healthmonitor set
------------------------------

Update a health monitor

.. program:: loadbalancer healthmonitor set
.. code:: bash

    openstack loadbalancer healthmonitor set
        [--name <name>]
        [--delay <delay>]
        [--expected-codes <codes>]
        [--http_method {GET,POST,DELETE,PUT,HEAD,OPTIONS,PATCH,CONNECT,TRACE}]
        [--timeout <timeout>]
        [--max-retries <max_retries>]
        [--max-retries-down <max_retries_down>]
        [--url-path <url_path>]
        [--type {PING,HTTP,TCP,HTTPS}]
        [--enable | --disable]
        <health_monitor>

.. option:: --name <name>

    Set health monitor name.

.. option:: --delay <delay>

    Set the time in seconds, between sending probes to members.

.. option:: --expected-codes <codes>

    Set the list of HTTP status codes expected in response from the member to declare it healthy.

.. option:: --http_method {GET,POST,DELETE,PUT,HEAD,OPTIONS,PATCH,CONNECT,TRACE}

    Set the HTTP method that the health monitor uses for requests.

.. option:: --timeout <timeout>

    Set the maximum time, in seconds, that a monitor waits to connect before it times out.
    This value must be less than the delay value.

.. option:: --max-retries <max_retries>

    The number of successful checks before changing the operating status of the member to ONLINE.

.. option:: --max-retries-down <max_retries_down>

    Set the number of allowed check failures before changing the operating status of the member to ERROR.

.. option:: --url-path <url_path>

    Set the HTTP URL path of the request sent by the monitor to test the health of a backend member.

.. option:: --type {PING,HTTP,TCP,HTTPS}

    Set the type of health monitor.

.. option:: --enable

    Enable health monitor.

.. option:: --disable

    Disable health monitor.

.. _loadbalancer_healthmonitor_set-health_monitor:
.. describe:: <health_monitor>

    Health monitor to update (name or ID).

loadbalancer healthmonitor delete
---------------------------------

Delete a health monitor

.. program:: loadbalancer healthmonitor delete
.. code:: bash

    openstack loadbalancer healthmonitor delete
        <health_monitor>

.. _loadbalancer_healthmonitor_delete-health_monitor:
.. describe:: <health_monitor>

   Health monitor to delete (name or ID).
