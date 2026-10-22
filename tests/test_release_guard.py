"""Release preflight against temporary git repositories, without network or data."""

import os
from pathlib import Path
import subprocess

GUARD = Path(__file__).resolve().parents[1] / ".github/scripts/resolve_release.sh"


def git(repo, *args):
    return subprocess.run(
        ["git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false",
         "-c", "user.name=CI Fixture", "-c", "user.email=ci@example.invalid", *args],
        cwd=repo, check=True, capture_output=True, text=True,
    )


def repository(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init")
    git(repo, "commit", "--allow-empty", "-m", "synthetic fixture")
    return repo


def resolve(repo, tmp_path):
    output = tmp_path / "output"
    result = subprocess.run(
        ["bash", str(GUARD)], cwd=repo, capture_output=True, text=True,
        env={**os.environ, "GITHUB_OUTPUT": str(output),
             "GITHUB_STEP_SUMMARY": str(tmp_path / "summary")},
    )
    return result, output.read_text() if output.exists() else ""


def test_no_tags_skips_publication_without_creating_a_tag(tmp_path):
    repo = repository(tmp_path)
    result, output = resolve(repo, tmp_path)
    assert result.returncode == 0
    assert output == "publish=false\n"
    assert git(repo, "tag", "--list").stdout == ""
    assert not (repo / "dist").exists()


def test_existing_tag_and_notes_are_resolved_read_only(tmp_path):
    repo = repository(tmp_path)
    notes = repo / "docs/release_notes/release_notes_1.2.3.md"
    notes.parent.mkdir(parents=True)
    notes.write_text("Synthetic release notes", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "synthetic release metadata")
    git(repo, "tag", "v1.2.3")
    before = git(repo, "status", "--porcelain").stdout
    result, output = resolve(repo, tmp_path)
    assert result.returncode == 0
    assert output == "publish=true\nversion=v1.2.3\n"
    assert git(repo, "status", "--porcelain").stdout == before
    assert git(repo, "tag", "--list").stdout == "v1.2.3\n"


def test_tag_without_notes_fails_instead_of_hiding_a_release_error(tmp_path):
    repo = repository(tmp_path)
    git(repo, "tag", "v1.2.3")
    result, output = resolve(repo, tmp_path)
    assert result.returncode != 0
    assert "publish=true" not in output
    assert "notes" in result.stderr
