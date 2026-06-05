"""
Helper script to run tests with proper configuration.
"""
import sys
import pytest

if __name__ == "__main__":
    # Run pytest with custom arguments
    args = [
        "tests/",
        "-v",
        "--tb=short",
        "-s",  # Show print statements
    ]

    # Add any command line arguments passed to this script
    if len(sys.argv) > 1:
        args.extend(sys.argv[1:])

    sys.exit(pytest.main(args))
