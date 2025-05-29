"""Test runner utilities for different test types."""
import sys

import pytest


def run_unit_tests():
  """Run only unit tests."""
  sys.exit(pytest.main(["-m", "unit", "-v", "--tb=short"]))


def run_e2e_tests():
  """Run only end-to-end tests."""
  sys.exit(pytest.main(["-m", "e2e", "-v", "--tb=short"]))


def run_all_tests():
  """Run all tests."""
  sys.exit(pytest.main(["-v", "--tb=short"]))
