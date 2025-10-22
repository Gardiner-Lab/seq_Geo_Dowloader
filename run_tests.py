#!/usr/bin/env python3
"""
Test runner script for RNA-seq downloader unit tests.

This script runs all unit tests and provides a summary of results.
It can be used for continuous integration or manual testing.
"""

import sys
import os
import subprocess
from pathlib import Path


def main():
    """Run all unit tests and display results."""
    print("=" * 60)
    print("RNA-seq Downloader Unit Tests")
    print("=" * 60)
    
    # Add src directory to Python path
    src_dir = Path(__file__).parent / 'src'
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))
    
    # Check if pytest is available
    try:
        import pytest
    except ImportError:
        print("Error: pytest is not installed.")
        print("Please install pytest: pip install pytest")
        return 1
    
    # Run tests with pytest
    test_args = [
        '-v',  # Verbose output
        '--tb=short',  # Short traceback format
        '--strict-markers',  # Strict marker checking
        'tests/',  # Test directory
    ]
    
    # Add coverage if available
    try:
        import pytest_cov
        test_args.extend(['--cov=src', '--cov-report=term-missing'])
        print("Running tests with coverage analysis...")
    except ImportError:
        print("Running tests without coverage (install pytest-cov for coverage analysis)...")
    
    print()
    
    # Run the tests
    exit_code = pytest.main(test_args)
    
    print()
    print("=" * 60)
    
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed.")
        print(f"Exit code: {exit_code}")
    
    print("=" * 60)
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())