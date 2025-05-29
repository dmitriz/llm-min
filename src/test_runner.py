"""Test runner utilities for different test types."""
import sys

import pytest


def run_unit_tests():
  """Run only unit tests."""
  return pytest.main(["-m", "unit", "-v", "--tb=short"])


def run_e2e_tests():
  """Run only end-to-end tests."""
  return pytest.main(["-m", "e2e", "-v", "--tb=short"])


def run_all_tests():
  """Run all tests."""
  return pytest.main(["-v", "--tb=short"])
