"""Tests for the RMF control mapper."""

import csv
import json
import sys
from pathlib import Path

import pytest

# Make scripts importable
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from map_controls import load_controls, load_evidence, determine_status, FRESHNESS_DAYS


def test_controls_load():
    controls = load_controls()
    assert len(controls) == 8
    ids = {c["id"] for c in controls}
    assert "AC-2" in ids
    assert "IA-2" in ids
    assert "AU-6" in ids


def test_evidence_load():
    evidence = load_evidence()
    assert "AC-2" in evidence
    assert "AU-6" in evidence
    assert evidence["AU-6"]["collected_date"] == "2026-08-12"


def test_status_implemented():
    evidence = load_evidence()
    status, reason = determine_status("AC-2", evidence)
    assert status in ("Implemented", "Partial")  # depends on freshness of sample data
    assert reason


def test_status_stale():
    evidence = load_evidence()
    status, reason = determine_status("AU-6", evidence)
    # AU-6 sample date is 2026-08-12 → should be stale relative to Nov 2026
    assert status == "Stale"
    assert "days old" in reason
