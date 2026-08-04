# ETL_MEDS_Template: A copier template for MEDS-Extract dataset ETL packages

[![test-template](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template/actions/workflows/test-template.yaml/badge.svg)](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template/actions/workflows/test-template.yaml)
[![code-quality](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template/actions/workflows/code-quality-main.yaml/badge.svg)](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template/actions/workflows/code-quality-main.yaml)
[![license](https://img.shields.io/badge/License-MIT-green.svg?labelColor=gray)](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template#license)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template/pulls)
[![DOI](https://zenodo.org/badge/901560475.svg)](https://doi.org/10.5281/zenodo.17536399)

This is a [copier](https://copier.readthedocs.io/) template for **config-only
[MEDS-Extract](https://github.com/mmcdermott/MEDS_extract) dataset ETL packages**: pip-installable
Python packages whose entire substance is one MESSY configuration file (declaring where a dataset's
raw data lives and how its rows map to MEDS events) registered with MEDS-Extract's generic runner.
Once such a package is published, converting the dataset to [MEDS](https://medical-event-data-standard.github.io/)
is a single command:

```bash
pip install MIMIC-IV-MEDS # for example
meds-extract-run spec=MIMIC-IV output_dir=/path/to/output
```

MEDS-Extract (v0.7+) handles everything at run time — staged raw-data download, the canonical
extraction pipeline, and version-provenance stamping — so the per-dataset package contributes only
its configuration, plus the packaging, CI, and citation scaffolding this template generates.

## Creating a new dataset ETL package

With [uv](https://docs.astral.sh/uv/) installed:

```bash
uvx copier copy gh:Medical-Event-Data-Standard/ETL_MEDS_Template my_dataset_MEDS
```

Answer the prompts (dataset name, package name, author info, ...), then follow the printed next
steps:

```bash
cd my_dataset_MEDS
git init -b main
uv lock && uv sync --group dev --group tests
uv run pre-commit install
# Fill in src/<package>/configs/event_configs.yaml, then:
uv run pytest tests/ -v
git add -A && git commit -m "Initial commit from ETL_MEDS_Template"
```

Commit everything the render produced, **including `uv.lock` and `.copier-answers.yml`** — the
latter is what lets `copier update` work later.

What you get:

- `src/<package>/configs/event_configs.yaml` — the MESSY file: a `sources:` block (where the raw
  data lives — HTTP, PhysioNet, or fsspec backends, with `${oc.env:...}` credential
  interpolation) plus the event-conversion tables. This file is yours; the template seeds it once
  and never overwrites it.
- A `pyproject.toml` registering the file under the `MEDS_extract.pipelines` entry-point group, so
  `meds-extract-run spec=<dataset name>` finds it by name and stamps your package's version into
  the output's provenance metadata.
- Tests: an offline check that the registered MESSY file resolves and parses (works for every
  dataset), plus — if you answered that your dataset has an open demo release — an end-to-end CI
  test running the full pipeline against it.
- CI (tests + pre-commit code quality), a tag-triggered PyPI publishing workflow (see
  [PyPI setup](#pypi) below), a seeded `README.md` and `CITATION.cff`, and an MIT license.

### What this template does *not* cover

Datasets that need custom *code* — pre-MEDS wrangling beyond what MESSY `_table.cols`/`_table.join`
transformations can express (e.g. archive unpacking or complex reshaping) — are out of scope for
the config-only shape. For those, write the pre-processing separately and run the standalone route
(`meds-extract-download` + `MEDS_transform-pipeline`) documented in
[MEDS-Extract](https://github.com/mmcdermott/MEDS_extract).

## Updating an existing package from the template

Template improvements (CI fixes, packaging conventions, new MEDS-Extract pins) propagate to
generated repositories via copier's update mechanism. In your dataset repository, with a clean git
tree:

```bash
uvx copier update
```

Review the diff, resolve any conflicts (your `event_configs.yaml`, `README.md`, and `CITATION.cff`
are never overwritten), and commit. Updates are pinned to this template's git tags, released per
[PEP 440](https://peps.python.org/pep-0440/) ordering.

## External services for your generated package

### PyPI

1. Go to [PyPI](https://pypi.org/) and make an account or log in as needed.
2. In your account settings, open the "Publishing" settings.
3. Set up a new "Trusted Publisher" for your GitHub repository (e.g., see the image below). Ensure
   the package name matches your `pyproject.toml`, and the workflow filename is
   `python-build.yaml`.
4. Then `git tag 0.1.0 && git push origin 0.1.0` publishes that version to PyPI and creates a
   signed GitHub release.

Example trusted publisher set-up:
![PyPI Trusted Publisher](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template/blob/main/static/pypi_trusted_publisher_example.png?raw=true)

### Zenodo

[Zenodo](https://zenodo.org/) can archive your releases and assign a citable DOI: follow
[GitHub's guide](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content),
then record the DOI in your `README.md` and `CITATION.cff`.

## Template development

```bash
uv sync
uv run pytest tests/ -v # renders the template and tests the rendered project
uv run pre-commit run --all-files
```

The template payload lives under [`template/`](template); questions and behavior are configured in
[`copier.yml`](copier.yml). Releases are git tags: tag the repository (PEP 440-ordered) whenever a
change should propagate to generated packages via `copier update`.
