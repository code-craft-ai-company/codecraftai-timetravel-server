# S8.6 — Configuration File and Environment Variable Support: Requirements

## Overview
Server configuration loadable from configuration files and/or environment variables, with sensible defaults and validation at startup.

## Requirements (EARS Notation)

### REQ-S8.6-001: Configuration File
The system shall load configuration from a YAML or TOML file at a path specified via `--config` CLI argument or `TIMETRAVEL_CONFIG` environment variable.

### REQ-S8.6-002: Environment Variables
The system shall support overriding configuration keys via environment variables with prefix `TIMETRAVEL_` (e.g., `TIMETRAVEL_LISTEN_PORT=9000`).

### REQ-S8.6-003: Precedence
Configuration precedence shall be: environment variables > configuration file > server defaults.

### REQ-S8.6-004: Startup Validation
WHEN the server starts, THE system SHALL validate all configuration values and exit with a descriptive error if any value is invalid.

## Acceptance Criteria
- Configuration loads from file, environment, and defaults with correct precedence. Invalid configuration produces a clear error at startup.
