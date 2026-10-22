"""Offline runner checks: only synthetic CSVs under pytest temporary directories."""

import pandas as pd
import pytest

from lib.io_guards import atomic_backup_write


def test_replacing_csv_preserves_previous_data(tmp_path):
    target = tmp_path / "joined" / "features.csv"
    original = pd.DataFrame({"synthetic_value": [1, 2]})
    replacement = pd.DataFrame({"synthetic_value": [3, 4]})
    atomic_backup_write(original, target)
    atomic_backup_write(replacement, target, backup_name="previous.csv")

    pd.testing.assert_frame_equal(pd.read_csv(target), replacement)
    pd.testing.assert_frame_equal(pd.read_csv(target.with_name("previous.csv")), original)


def test_dry_run_does_not_create_directories(tmp_path):
    target = tmp_path / "not-created" / "features.csv"
    atomic_backup_write(pd.DataFrame({"synthetic_value": [1]}), target, dry_run=True)
    assert not target.parent.exists()


def test_dry_run_does_not_modify_existing_csv_or_create_backup(tmp_path):
    target = tmp_path / "features.csv"
    target.write_text("synthetic_value\n1\n", encoding="utf-8")
    before = target.read_bytes()
    atomic_backup_write(pd.DataFrame({"synthetic_value": [2]}), target, dry_run=True)
    assert target.read_bytes() == before
    assert sorted(p.name for p in tmp_path.iterdir()) == ["features.csv"]


def test_failed_serialization_preserves_original_csv(tmp_path, monkeypatch):
    target = tmp_path / "features.csv"
    target.write_text("synthetic_value\n1\n", encoding="utf-8")
    before = target.read_bytes()

    def fail_serialization(self, destination, **kwargs):
        destination.write_text("incomplete", encoding="utf-8")
        raise OSError("simulated serialization failure")

    monkeypatch.setattr(pd.DataFrame, "to_csv", fail_serialization)
    with pytest.raises(OSError, match="simulated serialization failure"):
        atomic_backup_write(pd.DataFrame({"synthetic_value": [2]}), target)
    assert target.read_bytes() == before
