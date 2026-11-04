"""Tests of the copier template itself: rendering, conditional files, and the rendered project.

pytest-copie's ``copie`` fixture renders this repository's template from ``HEAD`` (with a dirty
working tree, the working copy), so these tests exercise unreleased template changes on every PR.
"""

import subprocess

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
        "src/Test_DS_MEDS/__init__.py",
        "src/Test_DS_MEDS/configs/__init__.py",
        "src/Test_DS_MEDS/configs/event_configs.yaml",
        "tests/test_configs.py",
    ):
        assert (project_dir / expected).exists(), f"Missing rendered file: {expected}"

    leftovers = [p for p in project_dir.rglob("*.jinja")]
    assert not leftovers, f"Unrendered .jinja files leaked into the project: {leftovers}"

    # has_demo defaults to False: no e2e test, and no demo sources bucket.
    assert not (project_dir / "tests" / "e2e_demo_test.py").exists()
    messy = (project_dir / "src" / "Test_DS_MEDS" / "configs" / "event_configs.yaml").read_text()
    assert "demo:" not in messy

    pyproject = (project_dir / "pyproject.toml").read_text()
    assert '"Test-DS" = "Test_DS_MEDS.configs:event_configs.yaml"' in pyproject
    assert 'name = "Test-DS-MEDS"' in pyproject

    workflow = (project_dir / ".github" / "workflows" / "python-build.yaml").read_text()
    assert "https://pypi.org/p/Test-DS-MEDS" in workflow
    assert "{{" not in workflow.replace("${{", ""), "Unrendered Jinja leaked into the workflow"


def test_render_with_demo(copie):
    project_dir = _render(copie, has_demo=True)
    assert (project_dir / "tests" / "e2e_demo_test.py").exists()
    messy = (project_dir / "src" / "Test_DS_MEDS" / "configs" / "event_configs.yaml").read_text()
    assert "demo:" in messy


def test_rendered_project_tests_pass(copie):
    """The rendered project must install (against MEDS-extract) and pass its own offline tests."""
    project_dir = _render(copie)

    def run(*argv):
        result = subprocess.run(argv, cwd=project_dir, capture_output=True, text=True)
        assert result.returncode == 0, (
            f"{argv} failed with exit code {result.returncode}.\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    run("git", "init", "-q", "-b", "main")
    run("uv", "lock")
    run("uv", "sync", "--group", "tests")
    run("uv", "run", "pytest", "tests/", "-v")
