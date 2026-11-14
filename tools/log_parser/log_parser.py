import csv
import math

from collections import defaultdict
from pathlib import Path


class LogParseError(Exception):
    """Raised when the log file contains invalid data."""


def analyze_log(file_path):
    """
    Analyze CAN message intervals from a CSV file.

    Required CSV columns:
        Timestamp, CAN ID, Data

    Returns:
        dict: Structured CAN log analysis results.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise LogParseError(f"Not a regular file: {path}")

    intervals = defaultdict(list)
    previous_timestamp = {}
    frame_counts = defaultdict(int)

    frame_count = 0

    with path.open(
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as f:

        reader = csv.DictReader(f)

        required = {"Timestamp", "CAN ID", "Data"}

        if not reader.fieldnames:
            raise LogParseError("CSV file is empty or has no header.")

        if not required.issubset(set(reader.fieldnames)):
            missing = required - set(reader.fieldnames)

            raise LogParseError(
                f"Missing required columns: {sorted(missing)}"
            )

        for row_number, row in enumerate(reader, start=2):

            if None in row:
                raise LogParseError(
                    f"Unexpected extra CSV fields at row {row_number}."
                )

            try:
                timestamp = float(row["Timestamp"])
            except (TypeError, ValueError):
                raise LogParseError(
                    f"Invalid timestamp at row {row_number}."
                )

            if not math.isfinite(timestamp):
                raise LogParseError(
                    f"Non-finite timestamp at row {row_number}."
                )

            can_id = row["CAN ID"].strip()

            if not can_id:
                raise LogParseError(
                    f"Empty CAN ID at row {row_number}."
                )

            frame_count += 1
            frame_counts[can_id] += 1

            if can_id in previous_timestamp:

                interval_ms = (
                    timestamp - previous_timestamp[can_id]
                ) * 1000

                if interval_ms < 0:
                    raise LogParseError(
                        f"Timestamp moved backwards for {can_id} "
                        f"at row {row_number}."
                    )

                intervals[can_id].append(interval_ms)

            previous_timestamp[can_id] = timestamp

    interval_analysis = {}

    for can_id, values in intervals.items():

        interval_analysis[can_id] = {
            "sample_count": len(values),

            "intervals_ms": [
                round(value, 3) for value in values
            ],

            "min_ms": round(min(values), 3),

            "max_ms": round(max(values), 3),

            "average_ms": round(
                sum(values) / len(values), 3
            )
        }

    return {
        "file": str(path),
        "frame_count": frame_count,

        "frame_count_by_can_id": dict(frame_counts),

        "interval_analysis": interval_analysis
    }
