"""
Dataset Test Runner Script.

This script provides a convenient interface for running the Living Voices
Dataset test suite with various options and configurations.

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py --coverage         # Run with coverage report
    python run_tests.py --fast             # Skip slow tests
    python run_tests.py --module integrity # Run specific module
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """
    Execute shell command and handle errors.
    
    Args:
        cmd: Command list to execute
        description: Human-readable description of command
        
    Returns:
        bool: True if command succeeded, False otherwise
    """
    print(f"\n{'=' * 60}")
    print(f"Running: {description}")
    print(f"{'=' * 60}\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n{description} completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nError: {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\nError: pytest not found. Please install with: pip install pytest")
        return False


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(
        description="Run Living Voices Dataset tests",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Generate coverage report'
    )
    
    parser.add_argument(
        '--fast',
        action='store_true',
        help='Skip slow tests (marked with @pytest.mark.slow)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='count',
        default=0,
        help='Increase verbosity (use -v or -vv)'
    )
    
    parser.add_argument(
        '--module', '-m',
        choices=['integrity', 'schema', 'statistics', 'quality', 'completeness'],
        help='Run specific test module'
    )
    
    parser.add_argument(
        '--json-report',
        action='store_true',
        help='Generate JSON test report'
    )
    
    parser.add_argument(
        '--html-report',
        action='store_true',
        help='Generate HTML coverage report'
    )
    
    args = parser.parse_args()
    
    # Change to tests directory
    tests_dir = Path(__file__).parent
    
    # Build pytest command
    cmd = ['pytest', str(tests_dir)]
    
    # Add verbosity
    if args.verbose:
        cmd.append('-' + 'v' * args.verbose)
    
    # Add coverage options
    if args.coverage:
        cmd.extend([
            '--cov=datasets',
            '--cov-report=term-missing'
        ])
        
        if args.html_report:
            cmd.append('--cov-report=html')
    
    # Skip slow tests if requested
    if args.fast:
        cmd.extend(['-m', 'not slow'])
    
    # Run specific module
    if args.module:
        module_map = {
            'integrity': 'test_data_integrity.py',
            'schema': 'test_metadata_schema.py',
            'statistics': 'test_statistics_accuracy.py',
            'quality': 'test_chunk_quality.py',
            'completeness': 'test_data_completeness.py'
        }
        cmd.append(str(tests_dir / module_map[args.module]))
    
    # Add JSON report
    if args.json_report:
        cmd.extend([
            '--json-report',
            '--json-report-file=test_results.json'
        ])
    
    # Run tests
    success = run_command(cmd, "Test Suite Execution")
    
    # Print summary
    print(f"\n{'=' * 60}")
    print("Test Summary")
    print(f"{'=' * 60}")
    
    if success:
        print("Status: PASSED")
        if args.coverage:
            print("\nCoverage report generated.")
            if args.html_report:
                print(f"HTML report: {tests_dir / 'htmlcov' / 'index.html'}")
        if args.json_report:
            print(f"JSON report: {tests_dir / 'test_results.json'}")
        return 0
    else:
        print("Status: FAILED")
        print("\nSome tests failed. Please review output above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
