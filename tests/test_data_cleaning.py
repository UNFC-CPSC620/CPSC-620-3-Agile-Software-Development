"""Unit and integration tests for data_cleaning.py.

This test suite covers:
- load_data: verifying file existence, error handling, empty file check.
- clean_data: validation, deduplication, price parsing, handling missing
  values, negative value removal, categorical standardization, and index reset.
- get_data_summary: statistical calculations, empty data handling, and validations.
- integration: end-to-end load -> clean -> summary pipeline.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

# Add the src folder to the system path to allow importing data_cleaning
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "CPSC-620-3-Agile-Software-Development-main" / "src"))

from data_cleaning import clean_data, get_data_summary, load_data


class TestLoadData(unittest.TestCase):
    """Test suite for load_data function."""

    def setUp(self):
        """Create a temporary directory for test CSV files."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_dir_path = Path(self.test_dir.name)

    def tearDown(self):
        """Clean up temporary directory."""
        self.test_dir.cleanup()

    def test_load_data_valid_file(self):
        """Test loading a valid CSV file."""
        sample_csv = self.test_dir_path / "valid_sample.csv"
        df_sample = pd.DataFrame({
            "price": [100, 200],
            "room_type": ["Private room", "Entire home/apt"],
            "neighbourhood": ["Harlem", "Midtown"],
            "minimum_nights": [1, 2]
        })
        df_sample.to_csv(sample_csv, index=False)

        loaded_df = load_data(sample_csv)
        self.assertIsInstance(loaded_df, pd.DataFrame)
        self.assertEqual(len(loaded_df), 2)
        self.assertListEqual(list(loaded_df.columns), list(df_sample.columns))

    def test_load_data_nonexistent_file(self):
        """Test loading a non-existent file raises FileNotFoundError."""
        nonexistent = self.test_dir_path / "does_not_exist.csv"
        with self.assertRaises(FileNotFoundError):
            load_data(nonexistent)

    def test_load_data_empty_file(self):
        """Test loading an empty CSV file raises ValueError."""
        empty_csv = self.test_dir_path / "empty.csv"
        # Create an empty file (0 bytes)
        empty_csv.write_text("")
        with self.assertRaises(Exception):
            load_data(empty_csv)

    def test_load_data_empty_dataframe(self):
        """Test loading a CSV file with only headers raises ValueError."""
        empty_df_csv = self.test_dir_path / "empty_df.csv"
        df_empty = pd.DataFrame(columns=["price", "room_type", "neighbourhood", "minimum_nights"])
        df_empty.to_csv(empty_df_csv, index=False)
        with self.assertRaises(ValueError):
            load_data(empty_df_csv)


class TestCleanData(unittest.TestCase):
    """Test suite for clean_data function."""

    def setUp(self):
        """Set up standard sample data for cleaning tests."""
        self.valid_data = pd.DataFrame({
            "price": ["$100.00", "200", "$1,500"],
            "room_type": ["entire home/apt", "Private room", "SHARED ROOM"],
            "neighbourhood": ["Brooklyn", "Queens", "Manhattan"],
            "minimum_nights": [1, 3, "2"]
        })

    def test_clean_data_type_validation(self):
        """Test that invalid input type raises TypeError."""
        with self.assertRaises(TypeError):
            clean_data("not a dataframe")
        with self.assertRaises(TypeError):
            clean_data([1, 2, 3])
        with self.assertRaises(TypeError):
            clean_data(None)

    def test_clean_data_missing_required_columns(self):
        """Test that missing required columns raise ValueError."""
        df_missing = pd.DataFrame({
            "price": [100],
            "room_type": ["Private room"]
            # Missing neighbourhood and minimum_nights
        })
        with self.assertRaises(ValueError) as context:
            clean_data(df_missing)
        self.assertIn("Missing required columns", str(context.exception))

    def test_clean_data_deduplication(self):
        """Test that duplicate rows are removed."""
        df_duplicate = pd.concat([self.valid_data, self.valid_data.iloc[[0]]], ignore_index=True)
        self.assertEqual(len(df_duplicate), 4)

        cleaned = clean_data(df_duplicate)
        self.assertEqual(len(cleaned), 3)

    def test_clean_data_price_formatting(self):
        """Test that prices formatted with currency symbols and commas are cleaned."""
        df = pd.DataFrame({
            "price": ["$1,250.00", " $75 ", "99.50"],
            "room_type": ["Entire home/apt", "Private room", "Private room"],
            "neighbourhood": ["Manhattan", "Brooklyn", "Queens"],
            "minimum_nights": [2, 1, 3]
        })
        cleaned = clean_data(df)
        self.assertEqual(cleaned["price"].iloc[0], 1250.0)
        self.assertEqual(cleaned["price"].iloc[1], 75.0)
        self.assertEqual(cleaned["price"].iloc[2], 99.5)
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned["price"]))

    def test_clean_data_invalid_price_dropped(self):
        """Test that non-numeric and non-positive prices are dropped."""
        df = pd.DataFrame({
            "price": ["invalid_price", 0, -50, "$150"],
            "room_type": ["Private room"] * 4,
            "neighbourhood": ["Queens"] * 4,
            "minimum_nights": [1, 1, 1, 1]
        })
        cleaned = clean_data(df)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned["price"].iloc[0], 150.0)

    def test_clean_data_invalid_minimum_nights_dropped(self):
        """Test that minimum_nights <= 0 or invalid values are removed."""
        df = pd.DataFrame({
            "price": [100, 100, 100, 100],
            "room_type": ["Private room"] * 4,
            "neighbourhood": ["Queens"] * 4,
            "minimum_nights": [0, -3, "invalid", 2]
        })
        cleaned = clean_data(df)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned["minimum_nights"].iloc[0], 2)

    def test_clean_data_missing_and_empty_values(self):
        """Test that NA and empty strings in required fields are removed."""
        df = pd.DataFrame({
            "price": [100, None, 150, 200, 250],
            "room_type": ["Private room", "Private room", "", "   ", "Entire home/apt"],
            "neighbourhood": ["Manhattan", "Brooklyn", "Queens", "Bronx", ""],
            "minimum_nights": [1, 2, 3, 4, 5]
        })
        cleaned = clean_data(df)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned["price"].iloc[0], 100.0)

    def test_clean_data_room_type_standardization(self):
        """Test that room types are standardized properly."""
        df = pd.DataFrame({
            "price": [100, 110, 120, 130],
            "room_type": ["entire home/apt", "PRIVATE ROOM", "  shared room  ", "hotel room"],
            "neighbourhood": ["Manhattan"] * 4,
            "minimum_nights": [1] * 4
        })
        cleaned = clean_data(df)
        expected_room_types = ["Entire home/apt", "Private room", "Shared room", "Hotel room"]
        self.assertListEqual(list(cleaned["room_type"]), expected_room_types)

    def test_clean_data_resets_index(self):
        """Test that the index of the returned DataFrame is properly reset."""
        df = pd.DataFrame({
            "price": [0, 100, 200],  # First row will be filtered out
            "room_type": ["Private room"] * 3,
            "neighbourhood": ["Brooklyn"] * 3,
            "minimum_nights": [1] * 3
        })
        cleaned = clean_data(df)
        self.assertListEqual(list(cleaned.index), [0, 1])


class TestGetDataSummary(unittest.TestCase):
    """Test suite for get_data_summary function."""

    def test_get_data_summary_valid(self):
        """Test summary computation on a valid cleaned DataFrame."""
        df = pd.DataFrame({
            "price": [100.0, 200.0, 300.0],
            "room_type": ["Private room", "Entire home/apt", "Private room"]
        })
        summary = get_data_summary(df)

        self.assertEqual(summary["total_listings"], 3)
        self.assertEqual(summary["average_price"], 200.0)
        self.assertEqual(summary["median_price"], 200.0)
        self.assertEqual(summary["room_types"]["Private room"], 2)
        self.assertEqual(summary["room_types"]["Entire home/apt"], 1)

    def test_get_data_summary_empty(self):
        """Test summary output when DataFrame is empty."""
        df_empty = pd.DataFrame(columns=["price", "room_type"])
        summary = get_data_summary(df_empty)

        self.assertEqual(summary["total_listings"], 0)
        self.assertIsNone(summary["average_price"])
        self.assertIsNone(summary["median_price"])
        self.assertEqual(summary["room_types"], {})

    def test_get_data_summary_type_error(self):
        """Test that non-DataFrame input raises TypeError."""
        with self.assertRaises(TypeError):
            get_data_summary("not a dataframe")

    def test_get_data_summary_missing_columns(self):
        """Test that missing required columns raise ValueError."""
        df = pd.DataFrame({"neighbourhood": ["Manhattan"]})
        with self.assertRaises(ValueError):
            get_data_summary(df)


class TestPipelineIntegration(unittest.TestCase):
    """End-to-end integration tests for data processing pipeline."""

    def setUp(self):
        """Create a temporary CSV file with dirty data."""
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_dir_path = Path(self.test_dir.name)
        self.raw_csv = self.test_dir_path / "raw_airbnb.csv"

        raw_df = pd.DataFrame({
            "price": ["$100.00", "$200.00", "$0", "$300.00", "$100.00", "invalid"],
            "room_type": ["entire home/apt", "private room", "shared room", "entire home/apt", "entire home/apt", "private room"],
            "neighbourhood": ["Midtown", "Williamsburg", "Astoria", "Harlem", "Midtown", "SoHo"],
            "minimum_nights": [1, 2, -1, 3, 1, 2]
        })
        raw_df.to_csv(self.raw_csv, index=False)

    def tearDown(self):
        """Clean up temporary directory."""
        self.test_dir.cleanup()

    def test_end_to_end_pipeline(self):
        """Test executing load -> clean -> summary on raw data."""
        raw_data = load_data(self.raw_csv)
        self.assertEqual(len(raw_data), 6)

        cleaned = clean_data(raw_data)
        # Expected dropped:
        # - Row 4 ($100 Midtown) is duplicate of Row 0
        # - Row 2 has price $0 and minimum_nights -1
        # - Row 5 has invalid price
        # Remaining: 3 valid listings (Row 0, 1, 3)
        self.assertEqual(len(cleaned), 3)

        summary = get_data_summary(cleaned)
        self.assertEqual(summary["total_listings"], 3)
        self.assertEqual(summary["average_price"], 200.0)  # (100 + 200 + 300) / 3
        self.assertEqual(summary["median_price"], 200.0)
        self.assertEqual(summary["room_types"]["Entire home/apt"], 2)
        self.assertEqual(summary["room_types"]["Private room"], 1)


if __name__ == "__main__":
    unittest.main()

