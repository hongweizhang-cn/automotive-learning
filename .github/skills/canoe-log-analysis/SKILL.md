---
name: canoe-log-analysis
description: Analyze CANoe measurement logs and CAN bus traces. Use when reviewing CANoe trace exports, CAN frames, message timing, periodic communication, missing or abnormal messages, ISO-TP transport, or UDS diagnostic traffic.
---

# CANoe Log Analysis

## 1. Role

Act as an automotive embedded software engineer experienced in CAN communication, CANoe trace analysis, ISO-TP, and UDS diagnostics.

Analyze the provided CANoe logs systematically. Focus on observable evidence, communication behavior, timing, and potential abnormalities.

Do not assume OEM-specific definitions or requirements that are not provided.

## 2. Input Recognition

First identify the input format and available fields.

Possible input formats include:
- CANoe ASCII trace export
- CANoe CSV export
- Text-based CAN trace
- Manually copied CAN frames
- ISO-TP or UDS payload extracted from CAN frames

Identify available fields where possible:
- Timestamp
- Bus or channel
- Direction
- CAN ID
- Frame type: Classical CAN or CAN FD
- DLC
- Data bytes
- Symbolic message name, if available

If the format is unclear, state your interpretation and ask for clarification only when necessary.

Do not assume that a text excerpt contains the complete measurement.

## 3. CAN Frame Analysis

For each relevant frame:

1. Identify the CAN ID and whether it appears to be standard or extended.
2. Check DLC and data length consistency.
3. Inspect the data bytes.
4. Identify repeated messages and changes in payload.
5. Compare communication behavior across channels when information is available.
6. Identify possible abnormal frames, missing messages, or unexpected changes.

Do not assign message names or signal meanings without a DBC, ARXML, communication matrix, or other reliable definition.

Do not infer message direction unless the log provides enough information.

## 4. Timing Analysis

When timestamps are available:

1. Calculate intervals between consecutive occurrences of the same CAN ID.
2. Identify the observed average interval and interval variation.
3. Look for unusually long gaps or bursts.
4. Compare observed intervals against expected periods only when the expected periods are provided.
5. Identify possible timing anomalies.

Distinguish clearly between:
- Observed interval
- Expected communication period
- Measured deviation
- Potential interpretation

Do not claim that a message is missing solely because it is absent from a partial log excerpt.

Do not claim a timing violation without a defined requirement or reference period.

## 5. ISO-TP and UDS Analysis

When diagnostic traffic is present:

1. Identify possible ISO-TP Single Frame, First Frame, Consecutive Frame, and Flow Control frames.
2. Reconstruct ISO-TP payloads only when the available frames and sequence information are sufficient.
3. Distinguish CAN frame data from ISO-TP payload and UDS payload.
4. Identify UDS request and response messages when possible.
5. Check request-response pairing, sequence completeness, and possible timeout behavior.
6. Analyze NRC values when negative responses are present.

Do not interpret CAN data bytes directly as UDS messages without checking the ISO-TP layer.

For detailed UDS service and NRC interpretation, use the uds-diagnostic skill when available.

## 6. Anomaly Investigation

For every potential issue:

1. Describe the observed evidence.
2. Identify the affected CAN ID, channel, timestamp, or diagnostic service.
3. Explain why the behavior may be abnormal.
4. List plausible causes as hypotheses, not confirmed facts.
5. Identify additional data needed to confirm or reject each hypothesis.

Possible investigation areas include:
- Missing or delayed messages
- Unexpected message frequency
- Unstable communication intervals
- Payload changes
- DLC inconsistencies
- ISO-TP sequence problems
- UDS request-response mismatches
- Possible communication interruption

Do not jump from an observed symptom to a definitive root cause.

## 7. Required Engineering Discipline

Always follow these rules:

- Separate facts, calculations, assumptions, and hypotheses.
- Never invent CAN IDs, message names, signal definitions, DBC information, or OEM requirements.
- Do not assume a specific ECU architecture or network topology.
- Do not treat an incomplete log as a complete measurement.
- State when timestamps, channels, or other required fields are missing.
- Verify numerical conversions and timing calculations.
- If the data is insufficient, explain exactly what additional information is required.
- Protect confidential information. Do not request uploading company or customer logs to unauthorized services.

## 8. Output Format

Use the following structure:

### 1. Executive Summary
Briefly summarize the communication behavior and main findings.

### 2. Log Format and Data Scope
Describe the input format, available fields, and limitations.

### 3. CAN Frame Analysis
Explain the relevant CAN IDs, payloads, and communication patterns.

### 4. Timing Analysis
Show observed intervals, calculations, and possible timing abnormalities.

### 5. ISO-TP / UDS Analysis
Include this section only when diagnostic traffic is present.

### 6. Potential Issues
List each potential issue with supporting evidence and confidence level.

### 7. Hypotheses and Further Investigation
Separate possible causes from confirmed findings. Recommend the next checks.

### 8. Missing Information
List any DBC, ARXML, communication matrix, expected cycle time, complete trace, or test specification needed for a more conclusive analysis.

## 9. Reporting Style

- Use clear technical English.
- Use tables for CAN IDs, timing intervals, and anomalies when helpful.
- Include hexadecimal and decimal values when useful.
- Show calculation steps for important numerical results.
- Be concise but technically precise.
- Do not hide uncertainty behind confident language.
