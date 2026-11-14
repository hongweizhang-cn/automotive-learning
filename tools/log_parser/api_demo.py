from log_parser import analyze_log


result = analyze_log("tools/log_parser/sample.csv")

print("Total frames:", result["frame_count"])

print(
    "CAN ID 0x100 frames:",
    result["frame_count_by_can_id"]["0x100"]
)

print(
    "CAN ID 0x100 intervals:",
    result["interval_analysis"]["0x100"]["intervals_ms"]
)
