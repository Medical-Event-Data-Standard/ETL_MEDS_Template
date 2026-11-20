"""Tests of the copier template itself: rendering, conditional files, and the rendered project.

pytest-copie's ``copie`` fixture renders this repository's template from ``HEAD`` (with a dirty
working tree, the working copy), so these tests exercise unreleased template changes on every PR.
"""

import subprocess
import tomllib

import yaml

ANSWERS = {
    "dataset_name": "Test-DS",
    "author_name": "CI Tester",
    "author_email": "ci@example.com",
}


def _render(copie, **extra):
    result = copie.copy(extra_answers={**ANSWERS, **extra})
    assert result.exit_code == 0, f"copier render failed: {result.exception}"
    assert result.exception is None
    assert result.project_dir is not None
    return result.project_dir


def test_render_defaults(copie):
    project_dir = _render(copie)

    for expected in (
        ".copier-answers.yml",
        "pyproject.toml",
        "README.md",
        "CITATION.cff",
        "LICENSE",
        ".gitignore",
        ".pre-commit-config.yaml",
        ".github/actions/setup/action.yaml",
        ".github/workflows/tests.yaml",
        ".github/workflows/code-quality-main.yaml",
        ".github/workflows/code-quality-pr.yaml",
        ".github/workflows/python-build.yaml",
        ".github/workflows/synthetic-etl.yaml",
        ".github/workflows/summary-stats.yaml",
        "scripts/summary_stats.sh",
        "src/Test_DS_MEDS/__init__.py",
        "src/Test_DS_MEDS/event_configs.yaml",
        "src/Test_DS_MEDS/sumeds_rules.yaml",
        "tests/conftest.py",
        "tests/e2e_synthetic_test.py",
        "tests/test_config.py",
        "tests/test_sumeds_rules.py",
        "tests/test_run_with_enrichment.py",
        "tests/regression/policy.yaml",
    ):
        assert (project_dir / expected).exists(), f"Missing rendered file: {expected}"

    leftovers = [p for p in project_dir.rglob("*.jinja")]
    assert not leftovers, f"Unrendered .jinja files leaked into the project: {leftovers}"

    # has_demo defaults to False: no e2e test, and no demo sources bucket.
    assert not (project_dir / "tests" / "e2e_demo_test.py").exists()
    messy = (project_dir / "src" / "Test_DS_MEDS" / "event_configs.yaml").read_text()
    assert "demo:" not in messy
    assert 'KINDS="full"' in (project_dir / "scripts" / "summary_stats.sh").read_text()

    # The suMEDS post-stages, in the order the fleet's specs use.
    assert yaml.safe_load(messy)["etl"]["post_stages"] == [
        "sumeds_link_unit_siblings",
        "sumeds_normalize_units",
        {"sumeds_enrich": {"rules": "Test-DS"}},
    ]
    assert (project_dir / "scripts" / "summary_stats.sh").stat().st_mode & 0o111, "not executable"

    pyproject = tomllib.loads((project_dir / "pyproject.toml").read_text())
    assert pyproject["project"]["name"] == "Test-DS-MEDS"
    entry_points = pyproject["project"]["entry-points"]
    assert entry_points["MEDS_extract.pipelines"] == {"Test-DS": "Test_DS_MEDS:event_configs.yaml"}
    assert entry_points["sumeds.rules"] == {"Test-DS": "Test_DS_MEDS:sumeds_rules.yaml"}
    assert pyproject["tool"]["setuptools"]["package-data"] == {"Test_DS_MEDS": ["*.yaml"]}

    workflow = (project_dir / ".github" / "workflows" / "python-build.yaml").read_text()
    assert "https://pypi.org/p/Test-DS-MEDS" in workflow
    for name in ("python-build", "synthetic-etl", "summary-stats"):
        text = (project_dir / ".github" / "workflows" / f"{name}.yaml").read_text()
        assert "{{" not in text.replace("${{", ""), f"Unrendered Jinja leaked into {name}.yaml"
        assert "{%" not in text, f"Unrendered Jinja leaked into {name}.yaml"
    synthetic = (project_dir / ".github" / "workflows" / "synthetic-etl.yaml").read_text()
    assert '"MESSY_synth==0.1.1"' in synthetic
    assert "./src/Test_DS_MEDS/event_configs.yaml" in synthetic
    assert "${{ matrix.python-version }}" in synthetic

    readme = (project_dir / "README.md").read_text()
    assert "## Breaking changes" in readme


def test_render_with_demo(copie):
    project_dir = _render(copie, has_demo=True)
    assert (project_dir / "tests" / "e2e_demo_test.py").exists()
    messy = (project_dir / "src" / "Test_DS_MEDS" / "event_configs.yaml").read_text()
    assert "demo:" in messy
    assert 'KINDS="full demo"' in (project_dir / "scripts" / "summary_stats.sh").read_text()


def test_rendered_project_tests_pass(copie):
    """The rendered project must install (MEDS-Extract and suMEDS) and pass its own offline tests: the toy ETL
    end to end, the spec checks and suMEDS's rules and enrichment contracts."""
    project_dir = _render(copie)

    def run(*argv):
        result = subprocess.run(argv, cwd=project_dir, capture_output=True, text=True)
        assert result.returncode == 0, (
            f"{argv} failed with exit code {result.returncode}.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    run("git", "init", "-q", "-b", "main")
    run("uv", "lock")
    run("uv", "sync", "--group", "dev")
    run("uv", "run", "pytest", "tests/", "-v")
