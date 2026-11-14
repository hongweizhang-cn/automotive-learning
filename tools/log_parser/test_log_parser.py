import tempfile
import unittest
from pathlib import Path

from log_parser import analyze_log, LogParseError


class TestAnalyzeLog(unittest.TestCase):

    def setUp(self):
        """Create a temporary directory for each test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.temp_path = Path(self.temp_dir.name)

    def write_csv(self, content):
        """Create a temporary CSV file."""
        path = self.temp_path / "test.csv"
        path.write_text(content, encoding="utf-8")
        return path

    def test_valid_log(self):
        """Test normal CSV analysis."""
        path = self.write_csv(
            "Timestamp,CAN ID,Data\n"
            "0.000,0x100,01 02\n"
            "0.020,0x100,03 04\n"
            "0.010,0x200,05 06\n"
            "0.040,0x100,07 08\n"
        )

        result = analyze_log(path)

        self.assertEqual(result["frame_count"], 4)

        self.assertEqual(
            result["frame_count_by_can_id"],
            {"0x100": 3, "0x200": 1}
        )

        self.assertEqual(
            result["interval_analysis"]["0x100"]["intervals_ms"],
            [20.0, 20.0]
        )

        self.assertEqual(
            result["interval_analysis"]["0x100"]["sample_count"],
            2
        )

        # A CAN ID with only one frame has no interval data.
        self.assertNotIn("0x200", result["interval_analysis"])

    def test_file_not_found(self):
        """Test missing file handling."""
        missing = self.temp_path / "missing.csv"

        with self.assertRaises(FileNotFoundError):
            analyze_log(missing)

    def test_missing_required_column(self):
        """Test missing CSV column."""
        path = self.write_csv(
            "CAN ID,Data\n"
            "0x100,01 02\n"
        )

        with self.assertRaisesRegex(
            LogParseError, "Missing required columns"
        ):
            analyze_log(path)

    def test_invalid_timestamp(self):
        """Test invalid timestamp."""
        path = self.write_csv(
            "Timestamp,CAN ID,Data\n"
            "abc,0x100,01 02\n"
        )

        with self.assertRaisesRegex(
            LogParseError, "Invalid timestamp"
        ):
            analyze_log(path)

    def test_non_finite_timestamp(self):
        """Test NaN timestamp."""
        path = self.write_csv(
            "Timestamp,CAN ID,Data\n"
            "NaN,0x100,01 02\n"
        )

        with self.assertRaisesRegex(
            LogParseError, "Non-finite timestamp"
        ):
            analyze_log(path)

    def test_timestamp_moves_backwards(self):
        """Test timestamp order validation."""
        path = self.write_csv(
            "Timestamp,CAN ID,Data\n"
            "0.020,0x100,01 02\n"
            "0.010,0x100,03 04\n"
        )

        with self.assertRaisesRegex(
            LogParseError, "Timestamp moved backwards"
        ):
            analyze_log(path)

    def test_empty_csv(self):
        """Test empty CSV file."""
        path = self.write_csv("")

        with self.assertRaisesRegex(
            LogParseError, "CSV file is empty"
        ):
            analyze_log(path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
