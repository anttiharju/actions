#!/usr/bin/env python3
"""
Test framework for the find-changes action.

This script discovers test cases from the testdata directory and runs them against action.py.
Each test case is defined as a JSON file with the following structure:
{
    "name": "Test case name",
    "description": "Description of what the test is verifying",
    "env": {
        "GITHUB_EVENT_NAME": "pull_request",
        "REGEX": ".*\\.py$",
        ...
    },
    "input_files": [
        {"path": "src/file1.py", "content": "..."}
    ],
    "expected_output": {
        "matrix": [
            {"name": "src", "path": "src", "file": "src/file1.py"}
        ]
    }
}
"""

import json
import os
import sys
import tempfile
import unittest
import subprocess


class FindChangesTestCase(unittest.TestCase):
    """Test case for the find-changes action."""

    def __init__(self, test_file, action_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_file = test_file
        self.action_path = action_path
        with open(test_file, "r") as f:
            self.test_data = json.load(f)
        self.test_name = self.test_data.get("name", os.path.basename(test_file))
        self._testMethodDoc = self.test_data.get("description", "")

    def runTest(self):
        """Run the test case."""
        # Create a temporary directory for the test
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set up the git repository
            self._setup_git_repo(temp_dir)

            # Create output file
            output_file = os.path.join(temp_dir, "github_output")
            with open(output_file, "w") as f:
                f.write("")

            # Set up the environment
            env = os.environ.copy()
            env.update(self.test_data.get("env", {}))
            env["GITHUB_OUTPUT"] = output_file

            # Run the action
            cmd = [sys.executable, os.path.join(self.action_path, "action.py")]
            result = subprocess.run(
                cmd, env=env, cwd=temp_dir, capture_output=True, text=True
            )

            # Check the output
            self.assertEqual(
                result.returncode, 0, f"Action failed with error: {result.stderr}"
            )

            # Parse the output file
            actual_output = self._parse_output_file(output_file)
            expected_output = self.test_data.get("expected_output", {})

            # Check the matrix output
            if "matrix" in expected_output:
                self.assertEqual(
                    actual_output.get("matrix", []),
                    expected_output["matrix"],
                    "Unexpected matrix output",
                )

    def _setup_git_repo(self, temp_dir):
        """Set up a git repository for testing."""
        # Initialize git repository
        subprocess.run(
            ["git", "init"],
            cwd=temp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=temp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=temp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Create initial commit
        with open(os.path.join(temp_dir, "initial.txt"), "w") as f:
            f.write("Initial commit")
        subprocess.run(
            ["git", "add", "."],
            cwd=temp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=temp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Create input files
        for file_info in self.test_data.get("input_files", []):
            file_path = os.path.join(temp_dir, file_info["path"])
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(file_info["content"])

        # Add and commit changed files
        subprocess.run(
            ["git", "add", "."],
            cwd=temp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        subprocess.run(
            ["git", "commit", "-m", "Add test files"],
            cwd=temp_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def _parse_output_file(self, output_file):
        """Parse the GitHub Actions output file."""
        result = {}
        with open(output_file, "r") as f:
            content = f.read()

        # Parse matrix output
        matrix_match = False
        matrix_lines = []
        for line in content.splitlines():
            if line == "matrix<<EOF":
                matrix_match = True
                continue
            elif matrix_match and line == "EOF":
                matrix_match = False
                continue
            elif matrix_match:
                matrix_lines.append(line)

        if matrix_lines:
            matrix_json = "\n".join(matrix_lines)
            result["matrix"] = json.loads(matrix_json)

        return result


def discover_tests(testdata_dir, action_path):
    """Discover test cases in the testdata directory."""
    test_cases = []
    for file in os.listdir(testdata_dir):
        if file.endswith(".json"):
            test_file = os.path.join(testdata_dir, file)
            test_case = FindChangesTestCase(test_file, action_path)
            test_cases.append(test_case)
    return test_cases


def main():
    """Main entry point."""
    # Get the path to the action.py file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    action_path = script_dir
    testdata_dir = os.path.join(script_dir, "testdata")

    # Print welcome message
    print("Running tests for the find-changes action")
    print(f"Test data directory: {testdata_dir}")

    # Discover and run tests
    test_cases = discover_tests(testdata_dir, action_path)
    if not test_cases:
        print("No test cases found in the testdata directory.")
        print("Create JSON test files in the testdata directory to run tests.")
        return

    # Create a test suite
    test_suite = unittest.TestSuite(test_cases)

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Exit with non-zero code if tests failed
    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    main()
