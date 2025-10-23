#!/usr/bin/env python3
"""
Test runner script for the personal website Flask application.
This script provides easy commands to run different types of tests.
"""

import sys
import subprocess
import argparse


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"\n[SUCCESS] {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[FAILED] {description} failed with exit code {e.returncode}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Test runner for personal website')
    parser.add_argument('--type', choices=['all', 'db', 'flask', 'coverage'], 
                       default='all', help='Type of tests to run')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Run tests in verbose mode')
    parser.add_argument('--no-warnings', action='store_true', 
                       help='Suppress warnings')
    
    args = parser.parse_args()
    
    # Base pytest command
    base_cmd = ['python', '-m', 'pytest']
    
    if args.verbose:
        base_cmd.append('-v')
    
    if args.no_warnings:
        base_cmd.extend(['--disable-warnings'])
    
    success = True
    
    if args.type == 'all':
        # Run all tests
        cmd = base_cmd.copy()
        success = run_command(cmd, "All Tests")
        
    elif args.type == 'db':
        # Run database tests only
        cmd = base_cmd + ['test_database.py']
        success = run_command(cmd, "Database Tests")
        
    elif args.type == 'flask':
        # Run Flask tests only
        cmd = base_cmd + ['test_projects.py']
        success = run_command(cmd, "Flask Application Tests")
        
    elif args.type == 'coverage':
        # Run tests with coverage
        cmd = base_cmd + ['--cov=.', '--cov-report=html', '--cov-report=term']
        success = run_command(cmd, "Tests with Coverage Report")
    
    if success:
        print(f"\n[SUCCESS] All tests completed successfully!")
        sys.exit(0)
    else:
        print(f"\n[FAILED] Some tests failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
