==================================
Automation Mojo TimeTravel Server
==================================

The ``automojo-timetravel-server`` package is a web service that provides a web interface for the ``automojo-timetravel-pod`` package. It is built on the ``automojo-webservice-flask`` stack and offers trace reception, persistence, remote debug control, and a web UI for time-travel debugging of instrumented applications.

Highlights
==========

- Persistence and data foundation: ORM models, credential store, server configuration model, and pluggable trace-data storage backends.
- Process lifecycle: service registration, unregistration, heartbeat reception, and a persistent process registry.
- Remote debug control: portal discovery, activation/deactivation, trace-configuration management, and debug-session coordination.
- Trace data reception: TCP and Unix-socket stream receivers, hybrid-format deserializer, back-pressure, and stream multiplexing.
- REST API and web UI: process management, portal control, trace configuration, debug sessions, and timeline/call-graph/variable views.
- Authentication, authorization, TLS, audit logging, and operational concerns (migrations, metrics, retention, graceful shutdown).

Repository Structure
====================

- ``development/`` - Runtime environment scripts.
- ``repository-setup/`` - Repository homing and setup scripts.
- ``source/packages/`` - Package source code.
- ``source/site/`` - Flask site and web UI assets.
- ``source/testroots/`` - TestBase test roots.
- ``specs/`` - Requirements and design documentation organised by feature layer.

Environment Setup
=================

When working in a Codex container:

.. code-block:: bash

   ./development/setup-agent-container

For local development:

.. code-block:: bash

   ./repository-setup/rehome-repository
   ./development/setup-envrionment

Running Tests
=============

Activate the virtual environment:

.. code-block:: bash

   source .venv/bin/activate

Run the single-host test suite:

.. code-block:: bash

   testbase testing run --root source/testroots/automojo --includes=automojo.tests.singlehost.timetravelserver --output=./.output

Standards and Conventions
=========================

- Feature specifications under ``specs/`` are organised by layer (``s0-*`` persistence, ``s1-*`` process lifecycle, ``s2-*`` remote control, and so on).

Additional Resources
====================

- Feature specification folders under ``specs/`` define each server subsystem in detail.
