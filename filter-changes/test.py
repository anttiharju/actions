#!/usr/bin/env python3

import unittest
import sys
import os
from unittest.mock import patch, mock_open

# Import functions from action.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from action import filter_changes, extract_glob_pattern


class TestFilterChanges(unittest.TestCase):
    def test_simple_glob_matches(self):
        """Test basic glob pattern matches."""
        # Test *.py pattern
        self.assertTrue(filter_changes("*.py", ["test.py"]))
        self.assertTrue(filter_changes("*.py", ["src/main.py"]))
        self.assertFalse(filter_changes("*.py", ["test.txt"]))

    def test_complex_glob_matches(self):
        """Test more complex glob patterns."""
        # Test {.github/*/*.yml,*/action.yml}
        self.assertTrue(
            filter_changes(
                "{.github/*/*.yml,*/action.yml}", [".github/workflows/ci.yml"]
            )
        )
        self.assertTrue(
            filter_changes("{.github/*/*.yml,*/action.yml}", ["custom/action.yml"])
        )
        self.assertFalse(
            filter_changes("{.github/*/*.yml,*/action.yml}", ["custom/config.yml"])
        )

        # Test .github/workflows/*.yml
        self.assertTrue(
            filter_changes(".github/workflows/*.yml", [".github/workflows/deploy.yml"])
        )
        self.assertFalse(
            filter_changes(".github/workflows/*.yml", [".github/actions/deploy.yml"])
        )

        # Test *{.md,.yml}
        self.assertTrue(filter_changes("*{.md,.yml}", ["README.md"]))
        self.assertTrue(filter_changes("*{.md,.yml}", ["config.yml"]))
        self.assertTrue(filter_changes("*{.md,.yml}", ["docs/guide.md"]))
        self.assertFalse(filter_changes("*{.md,.yml}", ["script.py"]))

    def test_multiple_files(self):
        """Test with multiple changed files."""
        changed_files = ["src/main.py", "README.md", "tests/test_app.js"]

        self.assertTrue(filter_changes("*.py", changed_files))
        self.assertTrue(filter_changes("*{.md,.yml}", changed_files))
        self.assertFalse(filter_changes(".github/workflows/*.yml", changed_files))

    @patch("subprocess.run")
    @patch("os.environ")
    def test_extract_glob_pattern(self, mock_environ, mock_subprocess_run):
        """Test extracting glob patterns from YAML using yq."""
        # Setup mock environment variables
        mock_environ.get = lambda key: {
            "yq": ".patterns",
            "file": "testdata/globs",
            "expression": "/tmp/expr_file",
        }.get(key)

        # Mock the subprocess.run call
        mock_process = mock_subprocess_run.return_value
        mock_process.stdout = "*.py\n"

        # Create a temporary file for the mock open
        with patch("builtins.open", mock_open()) as mock_file:
            result = extract_glob_pattern()

            # Verify file operations
            mock_file.assert_called_with("/tmp/expr_file", "w")
            mock_file().write.assert_called_once_with(".patterns")

            # Verify subprocess call
            mock_subprocess_run.assert_called_once()
            args, kwargs = mock_subprocess_run.call_args
            self.assertEqual(args[0][0], "yq")
            self.assertEqual(args[0][1], "--from-file")

            # Check the result
            self.assertEqual(result, "*.py")

    def test_real_glob_patterns_from_file(self):
        """Test with actual glob patterns from the globs file."""
        # Read patterns from the globs file
        with open("testdata/globs", "r") as f:
            patterns = [
                line.strip() for line in f if line.strip() and not line.startswith("#")
            ]

        # Test cases for each pattern
        test_cases = {
            "{.github/*/*.yml,*/action.yml}": {
                "should_match": [".github/workflows/ci.yml", "foo/action.yml"],
                "should_not_match": [
                    "action.yml",
                    ".github/file.yml",
                    "foo/workflow.yml",
                ],
            },
            ".github/workflows/*.yml": {
                "should_match": [
                    ".github/workflows/deploy.yml",
                    ".github/workflows/ci.yml",
                ],
                "should_not_match": [
                    ".github/actions/workflow.yml",
                    "workflows/test.yml",
                ],
            },
            "*{.md,.yml}": {
                "should_match": ["README.md", "config.yml", "docs/page.md"],
                "should_not_match": ["script.js", "image.png"],
            },
            "*.py": {
                "should_match": ["script.py", "src/main.py", "app/utils/helper.py"],
                "should_not_match": ["script.js", "requirements.txt"],
            },
        }

        # Verify each pattern against test cases
        for pattern in patterns:
            if pattern in test_cases:
                for file_path in test_cases[pattern]["should_match"]:
                    self.assertTrue(
                        filter_changes(pattern, [file_path]),
                        f"Pattern '{pattern}' should match '{file_path}'",
                    )

                for file_path in test_cases[pattern]["should_not_match"]:
                    self.assertFalse(
                        filter_changes(pattern, [file_path]),
                        f"Pattern '{pattern}' should not match '{file_path}'",
                    )


if __name__ == "__main__":
    unittest.main()
