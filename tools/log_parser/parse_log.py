import argparse
import json

from log_parser import analyze_log, LogParseError


def main():

    parser = argparse.ArgumentParser(
        description="Automotive CAN log analyzer"
    )

    parser.add_argument(
        "file",
        help="Path to CAN CSV log"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON"
    )

    args = parser.parse_args()

    try:
        result = analyze_log(args.file)

    except (FileNotFoundError, LogParseError) as error:
        parser.exit(1, f"Error: {error}\n")

    if args.json:

        print(json.dumps(result, indent=2))

    else:

        print(f"File: {result['file']}")
        print(f"Frames: {result['frame_count']}")

        for can_id, stats in result["interval_analysis"].items():

            print(f"\nCAN ID: {can_id}")

            print(
                f"Frames: "
                f"{result['frame_count_by_can_id'][can_id]}"
            )

            print(
                f"Intervals: {stats['intervals_ms']} ms"
            )

            print(f"Min: {stats['min_ms']} ms")
            print(f"Max: {stats['max_ms']} ms")
            print(f"Average: {stats['average_ms']} ms")


if __name__ == "__main__":
    main()
