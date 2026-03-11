# S4.2 — Timeline Reconstruction: Requirements

## Overview
Rebuilds chronological timelines from one or more trace data sources, aligning events to the gateway start timestamp. Supports merging traces from multiple portals or processes.

## Requirements (EARS Notation)

### REQ-S4.2-001: Timeline Building
WHEN events from a trace session are loaded, THE system SHALL sort them by `timestamp_offset` to produce a chronological timeline.

### REQ-S4.2-002: Multi-Source Merging
The system shall merge events from multiple data references (multiple portals, multiple processes) into a single unified timeline ordered by timestamp.

### REQ-S4.2-003: Time Range Selection
The system shall support selecting a sub-range of the timeline by start and end timestamp offsets.

### REQ-S4.2-004: Timeline Metadata
The system shall compute timeline metadata: total duration, event count, event type distribution, earliest and latest timestamps.

## Acceptance Criteria
- Events are ordered chronologically by timestamp_offset.
- Multi-source merge produces a correctly ordered unified timeline.
- Time range selection returns only events within the range.
