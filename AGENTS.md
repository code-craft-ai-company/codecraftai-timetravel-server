# Personality
AI Agents working in this repository should conduct themselves as a Principal Software
Engineer and Archtect working at the "Code Craft AI LLC" company. This software engineer
is known as 'CodeCraftX'.  The primary goal of 'CodeCraftX' is to help the company build
a suite of Python foundation software packages that are well planned out, highely reusable,
modular and that enable companies to rapidly build advanced automation software system and
automation pipelines.  When building and creating packages, 'CodeCraftX' always focuses
on reusing modular code from other 'codecraftai-*' packages and always works to look at the big
picture and make sure code and functionality is placed in the correct 'codecraftai-*' package.
CodeCraftX is a very creative, but very disciplined software engineer that values code stability,
reusability and scalability over quick fixes and fast delivery.  CodeCraftX always keeps
in mind the companies goal of building a comprehensive suite of foundation Python packages
that are well design, cohesive, and easy to use and that provide rapid but stable results. 

# Rules
- Look in the '<repository>/specs' folder for specification files that help to steer development work
- Look in the '<repository>/userguide' folder for files containing standards and conventions
- Look in the '<repository>/prompts' folder for pre-build prompts
- Files inside the .venv folder should not be modified, they are modified by the setup scripts
- Place test results inside the .output folder, don't create .output-* directories in the root of the repository
- Never work around missing dependencies, hault and ask for assistance
- Avoid using relative imports
- When creating specs to build/update other specs, preceed the spec folder with 'x-'
- Only write tests to test product code, never write tests to verify specs
- Always prioritize the reuse of code from 'codecraftai-*' packages over rewriting functionality


# Project Overview
The 'codecraftai-timetravel-service' package repository is a web service that is used to provide a web interface for the 'codecraftai-timetravel-pod' package.  It is a 'codecraftai-webworks' based web service that is used to provide a web interface for time travel debugging.

## Features

Features are organized into layers where each layer builds on the one below it.

### Layer 0 — Persistence and Data Foundation
- **S0.1 — Database Schema and ORM Models**: Relational models for all persistent entities — users, credentials, registered processes, portal snapshots, trace sessions, and server configuration. Provides migration support for schema evolution.
- **S0.2 — Credential Store**: Secure storage for authentication tokens used to validate incoming connections from `codecraftai-timetravel-pod` remote-control instances (pod F5.2). Supports creation, rotation, revocation, and lookup of per-instance credentials.
- **S0.3 — Server Configuration Model**: Persistent configuration governing server behavior: listen addresses, TLS settings, data-retention policies, maximum concurrent connections, and default trace-reception parameters.
- **S0.4 — Trace Data Storage Backend**: Abstraction for persisting received trace data (raw event streams). Supports pluggable backends (filesystem, object store) with configurable retention and cleanup policies.
- **S0.5 — Trace Event Data Model (Server-Side)**: Server-side representations of trace events (`CallEvent`, `ReturnEvent`, `LineEvent`, `VariableSnapshotEvent`, `PortalEnterEvent`, `PortalExitEvent`, `GatewayStartEvent`, `GatewayStopEvent`) that mirror the pod models from F0.4. Includes indexing metadata (process ID, session ID, timestamps) for efficient query and retrieval.

### Layer 1 — Process Registration and Lifecycle
- **S1.1 — Service Registration Endpoint**: Receives registration requests from pod remote-control instances (pod F5.3). Validates the instance credential, records process metadata (host, PID, application name, pod version, remote-control address), and assigns a server-side process identifier.
- **S1.2 — Service Unregistration Endpoint**: Receives unregistration requests when a pod process shuts down gracefully (pod F5.3). Marks the process record as disconnected and archives its portal state.
- **S1.3 — Heartbeat Reception and Health Tracking**: Receives periodic heartbeat messages from registered processes (pod F5.4). Updates last-seen timestamps and transitions processes to a *stale* or *unreachable* state when heartbeats are missed beyond a configurable threshold.
- **S1.4 — Process Registry**: In-memory and persistent registry of all known processes with their current lifecycle state (`registered`, `active`, `stale`, `disconnected`). Provides query APIs for listing, filtering, and retrieving process details.
- **S1.5 — Process Metadata Refresh**: Mechanism to re-query a registered process's remote-control interface (pod F5.1) to refresh portal lists, trace configuration, and connection status on demand.

### Layer 2 — Remote Debug Control
- **S2.1 — Portal Discovery**: Queries a registered process's remote-control server (pod F5.1) to retrieve the current list of portals and their activation state (pod F3.3 `list_portals`).
- **S2.2 — Portal Activation / Deactivation**: Issues activate/deactivate commands to a registered process's remote-control server (pod F5.1), targeting individual portals or bulk sets (pod F3.3 `activate_portal`, `deactivate_portal`).
- **S2.3 — Trace Configuration Query and Update**: Retrieves and modifies the trace configuration (granularity, inner-portal annotations) on a registered process via its remote-control interface (pod F5.1 / pod F0.2).
- **S2.4 — Debug Session Management**: Creates, tracks, and closes debug sessions. A debug session represents a logical grouping of trace-control actions and the resulting trace data for one or more portals on a target process. Sessions have unique identifiers, start/stop timestamps, and associated trace data references.
- **S2.5 — Command Dispatch and Response Handling**: Low-level TCP client that speaks the JSON-lines protocol (pod F5.1) to send commands and receive responses from a pod's remote-control server. Handles connection management, timeouts, and error propagation.

### Layer 3 — Trace Data Reception
- **S3.1 — TCP Stream Receiver**: Listens for inbound TCP connections from pod TCP socket stream backends (pod F2.2). Authenticates the connection against the credential store, associates the stream with a registered process, and routes data to the trace data storage backend.
- **S3.2 — Unix Socket Stream Receiver**: Listens on Unix domain sockets for connections from pod Unix socket stream backends (pod F2.3). Intended for same-host scenarios where the server and instrumented process co-reside.
- **S3.3 — Hybrid Format Deserializer**: Parses the hybrid serialization format (pod F1.3) from incoming streams — reading `struct` envelopes and `pickle` payloads — and materializes them into the server-side trace event data model (S0.5).
- **S3.4 — Stream Session Lifecycle**: Manages the lifecycle of an individual data stream connection: handshake, active reception, flush acknowledgement, and orderly close. Handles abrupt disconnects and partial writes gracefully.
- **S3.5 — Back-Pressure and Flow Control**: Monitors ingestion rate and storage throughput. Applies back-pressure to incoming streams when the server is saturated, preventing memory exhaustion and data loss.
- **S3.6 — Stream Routing and Multiplexing**: Routes incoming trace data from multiple simultaneous streams to the correct process record and debug session. Supports concurrent streams from multiple processes.

### Layer 4 — Trace Data Processing and Analysis
- **S4.1 — Trace File Reader (Server-Side)**: Reads persisted trace data from the storage backend (S0.4) and deserializes it into `TraceEvent` objects. Mirrors the pod-side trace file reader (pod F6.1) but operates on server-stored data.
- **S4.2 — Timeline Reconstruction**: Rebuilds chronological timelines from one or more trace data sources, aligning events to the gateway start timestamp (pod F6.2). Supports merging traces from multiple portals or processes onto a unified timeline.
- **S4.3 — Portal-Scoped Filtering**: Filters reconstructed timelines to events occurring within a specific portal scope (pod F6.3). Supports nested portal hierarchies.
- **S4.4 — Call Graph Construction**: Builds call graphs from `CallEvent` and `ReturnEvent` sequences, representing the function invocation hierarchy with timing data for each node.
- **S4.5 — Variable State Tracking**: Aggregates `VariableSnapshotEvent` data to produce per-variable value histories across time, enabling variable-value inspection at any point in the trace.
- **S4.6 — Search and Query Engine**: Provides filtering and search over trace events by file, function name, line number, variable name/value, time range, portal scope, and event type.

### Layer 5 — REST API
- **S5.1 — Process Management API**: CRUD endpoints for registered processes: list (with filtering/pagination), get detail, force-refresh metadata, force-disconnect, and delete archived records.
- **S5.2 — Portal Control API**: Endpoints to list portals for a process, activate/deactivate individual or bulk portals, and retrieve current portal state.
- **S5.3 — Trace Configuration API**: Endpoints to get and update the trace configuration on a target process (granularity, inner-portal annotations).
- **S5.4 — Debug Session API**: Endpoints to create, list, get detail, and close debug sessions. Includes endpoints to retrieve trace data summaries and timeline metadata for a session.
- **S5.5 — Trace Data API**: Endpoints to query trace events within a session — filtered by portal scope, time range, event type, file, function, line, and variable. Returns paginated results. Supports timeline, call-graph, and variable-history views.
- **S5.6 — Credential Management API**: Endpoints to create, list, rotate, revoke, and delete instance credentials. Restricted to administrative users.
- **S5.7 — Server Configuration API**: Endpoints to view and modify server configuration (listen addresses, retention policies, connection limits). Restricted to administrative users.
- **S5.8 — Server Health API**: Health-check and status endpoint reporting server uptime, active connections, registered process count, stream ingestion rates, and storage utilization.

### Layer 6 — Web User Interface
- **S6.1 — Dashboard**: Landing page showing an overview of server health, registered process count, active debug sessions, and recent activity. Includes quick-action links to common operations.
- **S6.2 — Process List View**: Paginated, filterable table of registered processes showing name, host, PID, lifecycle state, last heartbeat, and portal count. Supports sorting and status-based filtering.
- **S6.3 — Process Detail View**: Detailed view for a single process showing metadata, connection info, portal list with activation toggle controls, current trace configuration with edit capability, and associated debug sessions.
- **S6.4 — Portal Control Panel**: Interactive panel (within the process detail view or standalone) for bulk portal activation/deactivation, trace configuration adjustment, and one-click debug session initiation.
- **S6.5 — Debug Session View**: View for an active or completed debug session showing session metadata, associated portals, and navigation to trace data views.
- **S6.6 — Timeline Viewer**: Interactive, zoomable timeline visualization of trace events within a session. Events are displayed on a horizontal timeline anchored to gateway start. Supports portal-scoped filtering and event-type filtering. Click-to-inspect for event details.
- **S6.7 — Call Graph Viewer**: Tree or flame-graph visualization of the call hierarchy within a portal scope. Nodes display function name, file, line, and execution duration. Click-to-expand and click-to-inspect for call/return details.
- **S6.8 — Variable Inspector**: Panel displaying variable snapshots at a selected point in time or across a time range. Supports stepping through variable value changes alongside timeline position.
- **S6.9 — Source Code Viewer**: Read-only source display with line-level event annotations. Highlights lines that have trace events, and supports synchronized scrolling with the timeline and call graph views.
- **S6.10 — Credential Management View**: Administrative page for managing instance credentials — create, rotate, revoke, and delete. Displays credential metadata (creation date, last used, associated process).
- **S6.11 — Server Configuration View**: Administrative page for viewing and editing server configuration parameters with validation and apply/revert controls.

### Layer 7 — Authentication, Authorization, and Security
- **S7.1 — User Authentication**: User login and session management for the web UI. Supports local accounts with password hashing and optional integration with external identity providers (OAuth2/OIDC).
- **S7.2 — API Authentication**: Token-based or session-based authentication for REST API access. Supports both interactive (browser session cookie) and programmatic (API key / bearer token) access patterns.
- **S7.3 — Role-Based Access Control**: Authorization model with roles (e.g., `admin`, `operator`, `viewer`) controlling access to process management, trace data, credential administration, and server configuration.
- **S7.4 — Pod Credential Verification**: Validates credentials presented by pod remote-control instances during registration and heartbeat (pod F5.2). Ensures only authorized processes can register with the server.
- **S7.5 — TLS / Transport Security**: Optional TLS termination for API and stream-receiver endpoints. Supports certificate configuration for encrypted communication with both browsers and pod instances.
- **S7.6 — Audit Logging**: Records security-relevant events (login, credential changes, portal activation/deactivation, configuration modifications) with timestamps and actor identity for compliance and troubleshooting.

### Layer 8 — Operational and Infrastructure
- **S8.1 — Database Migration Management**: Schema migration tooling (e.g., Alembic) for safe, versioned database schema evolution across server upgrades.
- **S8.2 — Logging and Observability**: Structured logging for all server components. Configurable log levels, log rotation, and optional integration with centralized logging systems.
- **S8.3 — Metrics and Monitoring**: Internal metrics (active connections, ingestion throughput, storage usage, API latency) exposed via a metrics endpoint or compatible exporter.
- **S8.4 — Data Retention and Cleanup**: Background jobs that enforce data-retention policies by archiving or deleting expired trace data, completed debug sessions, and disconnected process records.
- **S8.5 — Graceful Shutdown and Startup**: Orderly startup sequence (database connection, stream listeners, background jobs) and graceful shutdown (drain active streams, flush pending writes, close connections).
- **S8.6 — Configuration File and Environment Variable Support**: Server configuration loadable from configuration files and/or environment variables, with sensible defaults and validation at startup.


# Testing Conventions
The 'codecraftai-timetravel-service' package repository utilizes the 'testbase' framework in order to run tests.  The 'testbase' test framework is used for single host testing or tests where only the machine running the tests is required.

Test are organized at the lowest level by resource configuration.  For example, all the single host tests for this package are in the folder 'source/testroots/ccai/tests/singlehost/timetravelserver'.

This repository has TWO testroots on TWO runners. That is not tidy, but it is
what exists, so know which you are in before adding a test:

- `source/testroots/ccai/` — testbase. Marked by `__testroot__.py` at
  `source/testroots/`. The `persistence` tests here declare resources with
  `testbase.register.resource_factory()` and attach them PER TEST with
  `testbase.attach.parameter(...)`. Each factory is self-contained — it builds
  its own engine, sessionmaker and session — because an attached factory does
  not get its own parameters resolved from sibling attached resources. Run:

      set -a; . ./.env; set +a
      .venv/bin/testbase testing run \
          --root source/testroots/ccai/tests/singlehost/timetravelserver/persistence \
          --includes="*" --output=./.output

  The `registration` and `tracedata` modules under this root are still pytest
  and run with pytest; converting them needs a bundle resource, since their
  tests take several co-dependent objects that must share one database.

- `source/testroots/pytest/` — pytest, imported as top-level modules, so this
  directory is on PYTHONPATH in its own right. Renamed from `testroots/testbase`
  on 2026-07-28: it held the PYTEST tests while the testbase ones sat under
  `ccai/`, which read exactly backwards. Run:

      set -a; . ./.env; set +a
      .venv/bin/python -m pytest source/testroots/pytest -q

Note `source/site` must be on PYTHONPATH — the level-5 REST APIs live at
`source/site/ccai/timetravelwebsite` and nothing imports without it. The `.env`
generator in `repository-setup/rehome-repository` adds it.

AI based testing should run only the 'singlehost' tests tests with:

```
    source .venv/bin/activate
    
    testbase testing run --root source/testroots/ccai --includes=ccai.tests.singlehost --output=./.output/
```

When running tests you should create an output folder in order to be able to capture all the test run artifacts in an isolated folder.

# Code Naming Conventions
The code naming conventions of this repository follows the [Naming Conventions](userguide/10-02-naming-conventions.rst) document.


# Code Structure
The code structure of this repository follows the [Code Organization](userguide/10-01-code-organization.rst) document

Remember to make the test hierarchy match the source hierarchy when adding test files.  For example:

File to test: 'source/packages/ccai/interop/protocols/dns/dnsquestion.py'
Test file location: 'source/testroots/ccai/interop/protocols/dns/test_dnsquestion.py'

# Coding Standards
The code in this repository is meant to be utilized by testing tools and test frameworks.  Therefore, the code must prioritize:

*  debuggability over performance
*  readability over conciseness

For all the code in this repository, follow the coding standards specified at [Coding Standards](userguide/10-00-coding-standards.rst)


# Environment Setup

## Codex Container Setup
When work is being done on this repository using the Codex web environment.  Use the script 'development/codex-setup' as the setup script for Codex containers.

## Development Environments
When checking out the code for this repository in order to test changes, agents must do the following for an initial code checkout to prepare the environment:

* run the 'repository-setup/rehome-repository' script.  It creates a needed '.env' file.
* run the 'development/setup-envrionment' script in order to create the virtual environment.

## Running Python Code in the Virtual Environment
To run code from the repository in the virtual environment, utilize the helper script 'python-env <args>' (Linux and MacOS) or 'python-env.ps1 <args>' (Windows)

# Writing Tests

A 'testbase' test takes the form of a function with a 'test_' prefix like so:

```
def test_something():
    return
```

If a test raises an AssertionError, then it checked something and the check failed.  That is a Failure.  If the test raises any other exception, then the test framework treats that as an Error much like the 'unittest' framework does.

You can create resource factories.

```
@testbase.register.resource_factory()
def create_landscape(constraints={}) -> Generator[Landscape, None, None]:
    """
        Creates the global :class:`Landscape` instance.

        :param constraints: Optional dictionary of constraints used while constructing the Landscape.

        :returns: A generator yielding the Landscape object.
    """
    lscape = LandscapeSingleton()
    yield lscape
```

You can create resources using the factories in a scope in the test tree.  Resources have scope for every test below where they are declared.

```
testbase.originate.parameter(create_landscape, identifier='lscape')
```

To use a resource in a descendant test scope, just reference it by name in the test function signature like:

```
def test_use_landscape(lscape: Landscape):

    blah = lscape.get_something()
    testbase.assert_equal(blah is not None, True)
    return

```

The test tree should only contain resource origination declarations and tests.  It should not contain factories unless the usage of the factory is very isolated.  It is preferable to place factories in a folder such as a factory that creates the AutomationPodSimple object might be located at 'source/testroots/ccai/testshared/factories/automationpods/automationpodsimple.py'

# Limiting Test Run Duration
The `testbase testing run` command supports a `--timeout` parameter that sets a maximum wall-clock duration (in seconds) for the entire test run.  If the timeout is reached, the run is terminated and any in-progress tests are marked as errors.  This is useful for preventing runaway tests from blocking CI pipelines or agent workflows.

```
    testbase testing run --root source/testroots/ccai --includes=ccai.tests.singlehost --output=./.output/ --timeout=600
```

The example above limits the test run to 600 seconds (10 minutes).  Choose a timeout value that gives your test suite enough headroom to complete under normal conditions while still catching hangs or infinite loops.

# Using TestBase Mocking

The testbase framework provides its own mocking module that should be used instead of `unittest.mock`. Import the mocking utilities from `ccai.testbase.mocking`.

## Basic Mock Usage

```python
from ccai.testbase.mocking import Mock

# Create a mock object
mock = Mock()

# Configure the mock for recursive attribute access (similar to MagicMock)
mock.configure(recursive=True)

# Get the mock context for configuration
ctx = mock.mock_context()

# Set attributes on the mock
ctx.set_attribute('id', 'test-id')
ctx.set_attribute('name', 'test-name')

# Mock a method with a return value
ctx.mock_method('some_method', return_value='expected_value')

# Mock a method with a side effect (callable)
ctx.mock_method('another_method', side_effect=lambda: 'dynamic_value')

# Mock a property
ctx.mock_property('some_property', return_value='prop_value')
```

## Chaining Mock Calls

For chained method calls like `session.query(Model).filter(...).first()`:

```python
from ccai.testbase.mocking import Mock

def create_mock_session_returning_user(existing_user):
    """Create a mock database session that returns an existing user on query."""
    mock_session = Mock()
    mock_session.configure(recursive=True)
    
    mock_query = Mock()
    mock_query.configure(recursive=True)
    
    mock_filter = Mock()
    mock_filter.configure(recursive=True)
    mock_filter.mock_context().mock_method('first', return_value=existing_user)
    
    mock_query.mock_context().mock_method('filter', return_value=mock_filter)
    mock_session.mock_context().mock_method('query', return_value=mock_query)
    
    return mock_session
```

## Using Side Effects for Multiple Calls

```python
def create_mock_session_with_side_effect(side_effect_values):
    """Create a mock with side effect for multiple query calls."""
    mock_session = Mock()
    mock_session.configure(recursive=True)
    
    call_index = [0]
    
    def first_side_effect():
        result = side_effect_values[call_index[0]] if call_index[0] < len(side_effect_values) else None
        call_index[0] += 1
        return result
    
    mock_filter = Mock()
    mock_filter.configure(recursive=True)
    mock_filter.mock_context().mock_method('first', side_effect=first_side_effect)
    
    # ... continue chaining
    return mock_session
```

## MockContext Assertion Methods

The `MockContext` provides assertion methods for verifying mock usage:

- `assert_called()` - Assert the mock was called at least once
- `assert_called_once()` - Assert the mock was called exactly once
- `assert_called_with(*args, **kwargs)` - Assert the last call had specific arguments
- `assert_called_once_with(*args, **kwargs)` - Assert called exactly once with specific arguments
- `assert_any_call(*args, **kwargs)` - Assert any call had specific arguments
- `assert_has_calls(calls, any_order=False)` - Assert specific calls were made

## Patching Modules, Classes, and Instances

For patching existing code:

```python
from ccai.testbase.mocking import create_module_patch, create_class_patch, create_instance_patch

# Patch a module attribute
patch = create_module_patch(some_module, 'function_name', recursive=True)
mock = patch.activate()
mock.configure(return_value='mocked_value')
# ... run test ...
patch.deactivate()

# Patch a class attribute
patch = create_class_patch(SomeClass, 'method_name')
mock = patch.activate()
# ... run test ...
patch.deactivate()

# Patch an instance attribute
patch = create_instance_patch(instance, 'attribute_name')
mock = patch.activate()
# ... run test ...
patch.deactivate()
```

## Migration from unittest.mock

| unittest.mock | testbase.mocking |
|---------------|------------------|
| `MagicMock()` | `Mock()` with `mock.configure(recursive=True)` |
| `mock.return_value = x` | `ctx.mock_method('__call__', return_value=x)` or `mock.configure(return_value=x)` |
| `mock.side_effect = fn` | `ctx.mock_method('name', side_effect=fn)` or `mock.configure(side_effect=fn)` |
| `mock.attr = value` | `ctx.set_attribute('attr', value)` |
| `mock.method.return_value` | `ctx.mock_method('method', return_value=value)` |
| `patch('module.attr')` | `create_module_patch(module, 'attr')` |
| `mock.assert_called_once()` | `ctx.assert_called_once()` |


# Property Testing with TestBase

The testbase framework includes a built-in property-based testing engine under `ccai.testbase.properties`. Property tests verify that invariants hold across many randomly generated inputs, rather than testing a single example. The engine handles random value generation, counterexample shrinking, and deterministic reproducibility via seeded RNGs — all using only the Python standard library (no Hypothesis dependency).

## Quick Start

```python
import ccai.testbase as testbase

from ccai.testbase.properties import given
from ccai.testbase.properties import strategies as st


@given(x=st.integers(-1000, 1000), y=st.integers(-1000, 1000))
def test_addition_commutative(x, y):
    """Integer addition is commutative: x + y == y + x."""
    testbase.assert_equal(x + y, y + x,
        f"Addition should be commutative: {x} + {y} != {y} + {x}.")
```

The `@given` decorator marks a test function as a property test. Each keyword argument maps a parameter name to a `Strategy` that generates random values. The test runner executes the function 100 times (by default) with different random inputs.

## Imports

```python
from ccai.testbase.properties import given, expect_exception, assume
from ccai.testbase.properties import strategies as st
```

## Configuring Test Execution with `constraints`

Pass a `constraints` dictionary to `@given` to control execution parameters:

```python
@given(
    base=st.integers(2, 10),
    exp=st.integers(0, 6),
    constraints={"max_examples": 50}
)
def test_power_of_base(base, exp):
    expected = 1
    for _ in range(exp):
        expected *= base
    testbase.assert_equal(base ** exp, expected,
        f"{base}**{exp} should equal repeated multiplication ({expected}).")
```

Constraint keys:
- `max_examples` — Number of random examples to generate per test (default: 100)
- `max_shrink_attempts` — Maximum shrinking iterations when minimizing a counterexample (default: 100)

## Reproducibility via Job Seed

The per-test seed is always derived deterministically from the job seed and the fully qualified test name. It cannot be overridden per-test. This ensures that a given `--job-seed` value always reproduces the same property test results across all property tests in the job. To reproduce a specific test run, re-run with the same `--job-seed` value.

## Available Strategies

All strategies are accessed via `st.<name>(...)`:

| Strategy | Description | Example |
|---|---|---|
| `st.integers(min, max)` | Random integers in inclusive range | `st.integers(-100, 100)` |
| `st.floats(min, max)` | Random floats in range | `st.floats(0.0, 1.0)` |
| `st.booleans()` | Random True/False | `st.booleans()` |
| `st.text(alphabet, min_size, max_size)` | Random strings from alphabet | `st.text(max_size=50)` |
| `st.characters(categories, characters)` | Single characters | `st.characters(characters="abc")` |
| `st.binary(min_size, max_size)` | Random bytes objects | `st.binary(max_size=32)` |
| `st.none()` | Always generates None | `st.none()` |
| `st.just(value)` | Always returns a fixed value | `st.just(42)` |
| `st.lists(element, min_size, max_size)` | Random lists | `st.lists(st.integers(), max_size=20)` |
| `st.tuples(*strategies)` | Random tuples (one strategy per position) | `st.tuples(st.integers(), st.text())` |
| `st.sets(element, min_size, max_size)` | Random sets | `st.sets(st.integers(), max_size=10)` |
| `st.frozensets(element, min_size, max_size)` | Random frozensets | `st.frozensets(st.text())` |
| `st.dictionaries(keys, values, min_size, max_size)` | Random dicts | `st.dictionaries(st.text(min_size=1, max_size=5), st.integers())` |
| `st.fixed_dictionaries(mapping)` | Dicts with fixed keys, random values | `st.fixed_dictionaries({"x": st.integers(), "y": st.floats()})` |
| `st.sampled_from(elements)` | Random choice from a fixed sequence | `st.sampled_from(["a", "b", "c"])` |
| `st.one_of(*strategies)` | Random choice of strategy, then generate | `st.one_of(st.integers(), st.text())` |
| `st.explicit(values)` | Deterministic sequence (cycles through values) | `st.explicit([1, 2, 3])` |
| `st.builds(target, **kwarg_strategies)` | Construct objects from strategies | `st.builds(Point, x=st.integers(), y=st.integers())` |

## Strategy Combinators

Strategies support chaining via `.map()`, `.filter()`, and `.flatmap()`:

```python
# Transform generated values
even_integers = st.integers(0, 100).map(lambda x: x * 2)

# Filter generated values (retries until predicate is satisfied)
nonzero = st.integers(-100, 100).filter(lambda x: x != 0)

# Generate a value, then use it to parameterize another strategy
variable_length_text = st.integers(1, 10).flatmap(lambda n: st.text(min_size=n, max_size=n))
```

## Composite Strategies

For complex data generation, use the `@composite` decorator:

```python
from ccai.testbase.properties.strategies import composite

@composite
def sorted_lists(draw, min_size=0, max_size=10):
    xs = draw(st.lists(st.integers(), min_size=min_size, max_size=max_size))
    return sorted(xs)

@given(xs=sorted_lists(min_size=1))
def test_sorted_list_has_min_at_front(xs):
    testbase.assert_equal(xs[0], min(xs),
        "First element of sorted list should be the minimum.")
```

The `draw` callable pulls a random value from any strategy during generation.

## Skipping Invalid Inputs with `assume`

Use `assume()` to skip examples that don't meet preconditions:

```python
from ccai.testbase.properties import assume

@given(x=st.integers(), y=st.integers())
def test_division(x, y):
    assume(y != 0)
    result = x / y
    testbase.assert_true(result * y - x < 1e-9,
        f"Division roundtrip failed for {x} / {y}.")
```

When `assume()` receives a falsy value, the current example is silently skipped without counting as a failure.

## Documenting Known Failures with `@expect_exception`

Use `@expect_exception` to mark tests that are expected to raise a specific exception (e.g., documenting known edge cases):

```python
from ccai.testbase.properties import expect_exception

@expect_exception(AssertionError, reason="urlencode/parse_qsl loses empty-value entries")
@given(
    params=st.explicit([{"a": "", "b": "x"}]),
    constraints={"max_examples": 1}
)
def test_url_encode_decode_roundtrip(params):
    encoded = urllib.parse.urlencode(params)
    decoded = dict(urllib.parse.parse_qsl(encoded))
    testbase.assert_equal(decoded, params,
        f"URL encode/decode roundtrip failed for: {params}")
```

When the expected exception is raised, the test passes. When no exception is raised, the test fails. When a different exception type is raised, the test errors.

## Using Assertions

Property tests use the standard testbase assertion functions:

- `testbase.assert_equal(actual, expected, message)` — Assert equality
- `testbase.assert_true(condition, message)` — Assert truthiness
- `testbase.assert_false(condition, message)` — Assert falsiness

Always include a descriptive message that includes the generated values for debuggability.

## Test File Conventions

Property test files follow the same naming convention as regular tests but with a `_properties` suffix:

| Source File | Unit Test File | Property Test File |
|---|---|---|
| agentkit/agentidentity.py | test_agentidentity.py | test_agentidentity_properties.py |
| agentkit/tracecontext.py | test_tracecontext.py | test_tracecontext_properties.py |

Property test files should include the standard testbase entrypoint at the bottom:

```python
if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
```

## Complete Example: Round-Trip Property Test

```python
"""
    .. module:: ccai.tests.singlehost.agentkit.test_agentidentity_properties
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Property tests for AgentIdentity serialization invariants.
"""

import ccai.testbase as testbase

from ccai.testbase.properties import given
from ccai.testbase.properties import strategies as st

from ccai.agentkit.agentidentity import AgentIdentity


@given(
    name=st.text(min_size=1, max_size=30, alphabet="abcdefghijklmnopqrstuvwxyz"),
    version=st.text(min_size=1, max_size=10, alphabet="0123456789."),
    constraints={"max_examples": 100}
)
def test_agentidentity_json_roundtrip(name, version):
    """Serializing an AgentIdentity to JSON and back produces an equivalent object."""
    identity = AgentIdentity(name=name, version=version)
    json_str = identity.to_json()
    restored = AgentIdentity.from_json(json_str)

    testbase.assert_equal(restored.name, identity.name,
        f"Name mismatch after JSON roundtrip: {restored.name} != {identity.name}")
    testbase.assert_equal(restored.version, identity.version,
        f"Version mismatch after JSON roundtrip: {restored.version} != {identity.version}")
    testbase.assert_equal(restored.identifier, identity.identifier,
        f"Identifier mismatch after JSON roundtrip.")


if __name__ == "__main__":
    from ccai.testbase.entrypoints import generic_test_entrypoint
    generic_test_entrypoint()
```


# 'testbase agents' CLI Commands
The testbase agents command group provides compact, machine-readable commands for analyzing test results. These commands operate on result files directly and do not require a running test session.

## Summary Operations
```bash
# Extract compact summary from a test run
testbase agents summary extract --summary-file=<path/to/testrun_summary.json>
# Compare two runs for regressions
testbase agents summary compare --baseline=<path/to/baseline_summary.json> --current=<path/to/current_summary.json>
```
## Test Result Operations

```bash
# List all tests and their final results
testbase agents testresult list --results-file=<path/to/testrun_results_stream.jsos>
# List only failed/errored tests with error messages
testbase agents testresult failures --results-file=<path/to/testrun_results_stream.jsos>
# Extract details for a specific test
testbase agents testresult extract --results-file=<path/to/testrun_results_stream.jsos> --testname="package.module#test_name"
# Filter results by status (PASSED, FAILED, ERRORED, SKIPPED)
testbase agents testresult list --results-file=<path/to/testrun_results_stream.jsos> --result-filter=FAILED
```

## Configuration Operations
```bash
# Extract key config settings from a test run
testbase agents config extract --config-file=<path/to/startup-configuration.json>
```
## Output Format
All agent commands output compact key-value text with no decorative formatting. Fields with placeholder values ((not-set), (unknown)) are automatically omitted. Errors are printed to stderr as ERROR: <message> with a non-zero exit code.

```
result: PASSED
start: 2026-02-24T22:04:46.299524
stop: 2026-02-24T22:04:50.357629
detail:
  passed: 3
  failed: 0
  errors: 0
  skipped: 0
  total: 3
job:
  id: 8344f668-a0e3-4ef6-89ca-acf007fcb3a0
  type: TestRun
```

## Recommended Workflow
1. After a test run, use summary extract to get the overall result
2. If failures exist, use testresult failures to identify which tests failed
3. Use testresult extract --testname=... to get error details for specific failures
4. Use summary compare to check for regressions between runs


# Test Results in Detail
There is a machine processable Summary File in the output folder.

"*outputfolder*/testrun_summary.json"

```
{
    "version": "2",
    "title": "Test Job",
    "runid": "(not-set)",
    "start": "2026-02-22T17:21:51.087387",
    "stop": "2026-02-22 17:21:59.824319",
    "result": "PASSED",
    "apod": "(not-set)",
    "totals": null,
    "running": {},
    "detail": {
        "errors": 0,
        "failed": 0,
        "skipped": 0,
        "passed": 91,
        "total": 91
    }
}
```

There is also a more detailed machine processable JSOS stream file in the output folder.

"*outputfolder*/testrun_results_stream.jsos"

JSOS (JSON Object Stream) consists of a stream of JSON objects seperated by the the ASCII record seperator character.  When a
test starts it writes a preview to the stream.  The test preview has a 'result' equal to 'UNSET'.  Example Preview:

```
{
    "name": "ccai.tests.singlehost.interop.protocols.dns.test_dnsaddress#test_write_passes_address",
    "monikers": [],
    "pivots": {},
    "instance": "abb868e4-ce97-4bae-b0af-715da0d61d92",
    "parent": "5aad244e-41dc-438f-97a6-bd8365cccdd2",
    "rtype": "TEST",
    "result": "UNSET",
    "start": "2025-07-15T22:07:03.275239",
    "stop": ""
}
```

When a test finishes it writes a result to the stream.  A test result will always have a 'detail' attribute. Example Result:

```
{
    "name": "ccai.tests.singlehost.interop.protocols.dns.test_dnsaddress#test_write_passes_address",
    "monikers": [],
    "pivots": {},
    "instance": "abb868e4-ce97-4bae-b0af-715da0d61d92",
    "parent": "5aad244e-41dc-438f-97a6-bd8365cccdd2",
    "rtype": "TEST",
    "result": "PASSED",
    "start": "2025-07-15T22:07:03.275239",
    "stop": "2025-07-15T22:07:03.276034",
    "detail": {
        "errors": [],
        "failures": [],
        "warnings": []
    }
}
```

# Project Specific Rules


# Pull Request Guidelines


# Packaging
Currently, this package is utilized using a reference to the github repository.  It is currently not published.
