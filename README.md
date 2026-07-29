# MEDS-ETL-Template: Convert your custom dataset to MEDS via MEDS-Extract

[![codecov](https://codecov.io/gh/Medical-Event-Data-Standard/ETL_MEDS_Template/graph/badge.svg?token=RW6JXHNT0W)](https://codecov.io/gh/Medical-Event-Data-Standard/ETL_MEDS_Template)
[![tests](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template/actions/workflows/tests.yaml/badge.svg)](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template/actions/workflows/tests.yaml)
[![code-quality](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template/actions/workflows/code-quality-main.yaml/badge.svg)](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template/actions/workflows/code-quality-main.yaml)
![python](https://img.shields.io/badge/-Python_3.12-blue?logo=python&logoColor=white)
[![license](https://img.shields.io/badge/License-MIT-green.svg?labelColor=gray)](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template#license)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template/pulls)
[![contributors](https://img.shields.io/github/contributors/Medical-Event-Data-Standard/ETL_MEDS_Template.svg)](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template/graphs/contributors)
[![DOI](https://zenodo.org/badge/901560475.svg)](https://doi.org/10.5281/zenodo.17536399)

This is a template repository for a [MEDS-Extract](https://github.com/mmcdermott/MEDS_extract) powered
extraction pipeline for a custom dataset. Once you have customized the repository to your dataset (see
instructions below), you will be able to run your extraction pipeline with a few simple command-line
commands, such as:

```bash
pip install PACKAGE_NAME # you can do this locally or via PyPI
# Download your data or set download credentials
COMMAND_NAME root_output_dir=$ROOT_OUTPUT_DIR
```

See the [MIMIC-IV MEDS Extraction ETL](https://github.com/Medical-Event-Data-Standard/MIMIC_IV_MEDS) for a
real-world example, or the
[MEDS-Extract example](https://github.com/mmcdermott/MEDS_extract/tree/main/example) for a small synthetic
dataset you can run end-to-end to understand the extraction pipeline before customizing this template.

## How to use this repository

1. Initialize a new repository using this template repository.
2. Rename the directory after `src/` to the name of your package in python-friendly format (e.g.,
   `MIMIC_IV_MEDS`).
3. Customize the following external services:
   - [CodeCov](#codecov)
   - [PyPI](#pypi)
   - [Zenodo](#zenodo)
4. Customize the following code points:
   - [`pyproject.toml`](#pyprojecttoml)
   - [`src/.../__init__.py`](#srcinitpy)
   - [`src/.../configs/main.yaml`](#srcconfigsmainyaml)
   - [`src/.../pre_MEDS.py`](#srcpre_medspy)
   - [`src/.../configs/event_configs.yaml`](#srcconfigsevent_configsyaml)
   - [`README.md`](#readmemd)
   - [`tests/e2e_demo_test.py`](#testse2e_demo_testpy)
   - [`.pre-commit-config`](#pre-commit-config)
   - [`CITATION.cff`](#citationcff)

### External Services

#### CodeCov

1. Go to [CodeCov](https://codecov.io/) and add make an account or log-in as needed.
2. Follow the instructions to configure your new repository with CodeCov.
3. Copy the badge markdown from CodeCov and paste it into the `README.md` file. To find the badge markdown
   link, go to your repository in CodeCov, click on the "Configuration" tab, click on the "Badges and
   Graphs" option, then copy the markdown link from the top section and paste it in the corresponding line
   of the README, in place of the default link included above.
4. It will now track the test coverage of your ETL, including running the full pipeline against the demo
   data you provide in the `demo` bucket of the `sources:` block in `event_configs.yaml`.

#### PyPI

1. Go to [PyPI](https://pypi.org/) and add make an account or log-in as needed.
2. Go to your account settings and go to the "Publishing" settings.
3. Set up a new "Trusted Publisher" for your GitHub Repository (e.g., see the image below). Ensure your
   package name matches in the trusted publisher and in your `pyproject.toml` file!
4. Now, if, on the local command line, you run `git tag 0.0.1`, then `git push origin 0.0.1`, it will push a
   new, tagged version of your code as of the local commit when you ran the command both to a new GitHub
   Release and to PyPI. This will allow you to install your package via `pip install PACKAGE_NAME` and to manage
   versions effectively!

Example trusted publisher set-up:
![PyPI Trusted Publisher](https://github.com/Medical-Event-Data-Standard/ETL_MEDS_Template/blob/main/static/pypi_trusted_publisher_example.png?raw=true)

#### Zenodo

Zenodo provides a way to archive your code and assign a DOI to it for citation purposes. This is optional, but
if you do not set it up, be sure to remove the DOI badge from the `README.md` file and the DOI field
`CITATION.cff` file (which are both currently linked to the template repository's Zenodo archive). To set up
Zenodo, simply follow
[these
instructions](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content)
and a Zenodo record will be created for your package upon first release. Once created, update the DOI badge in
the `README.md` file to reflect your new DOI (you can click on the DOI badge image in the Zenodo page to get a
replacement markdown string to use in your new package).

### Code Points:

#### `pyproject.toml`

In the `pyproject.toml` file, you will need to update the following fields:

1. Under `[project]`:
   - `name = "ETL-MEDS"`: Update `ETL-MEDS` to the name of your package (e.g., `MIMIC-IV-MEDS`)
   - `authors = [...]`: Update the author information to your name and email.
   - `description = "..."`: Update the description to a brief description of your dataset.
   - `dependencies = [...]`: Update the dependencies to include the necessary packages for your ETL pipeline
     (if any additional packages are needed).
2. Under `[project.scripts]`
   - `MEDS_extract-sample_dataset = "ETL_MEDS.__main__:main"`: Update `MEDS_extract-sample_dataset` to the
     name of your command-line pipeline (e.g., `MIMIC-IV_extract`) and update `ETL_MEDS` to the name of your
     package that you would import in python (e.g., `MIMIC_IV_MEDS`). This will be the same as the directory
     name between `src` and your actual code.
3. Under `[project.urls]`
   - `Homepage = "..."` Update the homepage to the URL of your GitHub repository.
   - `Issues = "..."` Update the issues URL to the URL of your GitHub repository issues page.

#### `src/.../__init__.py`

In this file, you simply need to update the `__package_name__ = "ETL_MEDS"` line to refer not to `ETL_MEDS`
but to your new package import name (e.g., `MIMIC_IV_MEDS`)

#### `src/.../configs/main.yaml`

In this file, update the dataset metadata that will be recorded in the extracted output's
`metadata/dataset.json`:

1. `dataset_name`: The name of the dataset.
2. `raw_dataset_version`: The version of the raw dataset this version of your pipeline is designed to work
   with.

Where your raw data is downloaded from is configured separately, in the `sources:` block of
[`event_configs.yaml`](#srcconfigsevent_configsyaml).

#### `pre_MEDS.py`

This script should be generally modified to include any "pre-MEDS" steps that are necessary to prepare the
dataset for MEDS-Transforms based extraction. Critically, these steps often include:

1. De-compressing files or otherwise preparing the raw data for extraction at a technical level.
2. Joining tables together so that all relevant rows include the unifying `subject_id` (though simple joins
   can also be expressed directly in `event_configs.yaml` via `_table.join` blocks).
3. Converting any offsets into timestamps.
4. Any other modifications of interest.

The sample implementation simply copies the raw files through unchanged (so the sample pipeline is runnable
end-to-end); replace it with your dataset's real pre-MEDS logic, or **delete the file entirely** if your
dataset needs no pre-MEDS wrangling — the pipeline will then run extraction directly against the raw input
directory.

See [MEDS-Extract](https://meds-extract.readthedocs.io/) for more documentation on the appropriate
construction of the pre-MEDS script.

#### `src/.../configs/event_configs.yaml`

This file is the combined MESSY (MEDS-Extract Specification Syntax YAML) configuration file for your
dataset. It carries two things: a `sources:` block declaring where your raw data can be downloaded from, and
the event-conversion configuration mapping rows of your raw data tables to MEDS events.

##### The `sources:` block

Raw data downloading is handled by MEDS-Extract's `meds-extract-download` CLI (which the pipeline command
invokes for you when `do_download=True`), driven by the `sources:` block of this file. The block contains
named buckets of sources:

1. `dataset`: The sources for the full dataset.
2. `demo`: The sources for a smaller, open, demo version of the dataset (used when `do_demo=True`).
3. `common`: Shared metadata files or other shared resources, fetched regardless of which bucket is
   selected.

Each bucket is a list of source definitions with a `type:` of `http` (explicit URL lists), `physionet` (any
PhysioNet release, driven by its `SHA256SUMS.txt`, with authentication support), or `fsspec` (local or
cloud mirrors of pre-downloaded data). All backends support `include:`/`exclude:` filename globs. For
example, for a credentialed PhysioNet dataset:

```yaml
sources:
  dataset:
    - type: physionet
      base_url: https://physionet.org/files/YOUR_DATASET/1.0
      username: ${oc.env:PHYSIONET_USERNAME}
      password: ${oc.env:PHYSIONET_PASSWORD}
```

We _strongly_ recommend that you _do not_ include your username and password literally in the file.
Instead, use `${oc.env:...}` OmegaConf resolvers as above to reference environment variables. MEDS-Extract
strips the `sources:` block from all logged and output-directory copies of the config, so credentials
referenced this way never land in logs or shared outputs.

If your dataset cannot be downloaded automatically at all, remove the `sources:` block, set
`do_download=False` (in `configs/main.yaml` or on the command line), and place your raw data files manually
in the `raw_input_dir`.

##### Event conversion

Event field values like `code` and `time` are written as [dftly](https://github.com/mmcdermott/dftly)
expressions. Key syntax elements:

- **Column references**: `$column_name` (e.g., `$test_name`)
- **String interpolation**: `f"PREFIX//{$col1}//{$col2}"` (using `//` as the MEDS code separator). Null
  components null-propagate, dropping the row; write `f"{$col ?? 'UNK'}//..."` to fill nulls and keep the
  row instead.
- **Time parsing**: `$timestamp::"%Y-%m-%d %H:%M:%S"` parses strictly (unparsable non-null values are an
  error); `$timestamp::?"%Y-%m-%d %H:%M:%S"` parses leniently (rows that parse under no format are dropped,
  with a per-event WARNING and count in the logs).
- **Bare words**: literal string values (e.g., `code: MEDS_BIRTH`)
- **Static events**: `time: null`
- **Inherited fields**: the top-level `_defaults:` block sets fields inherited by every table — most
  importantly `subject_id`, a dftly expression computing the MEDS subject ID (omit it entirely if your
  tables literally have a `subject_id` column).
- **Whole-table modifications**: a per-table `_table:` block holds `cols:` (derived columns, which may
  reference earlier entries) and `join:` (joining another table in to, e.g., recover the subject ID, as the
  sample's `labs_vitals` table demonstrates).
- **Code metadata**: per-event `_metadata:` blocks populate the extracted `metadata/codes.parquet` from
  reference tables (see the sample's `lab_descriptions` and `medication_classes` usages).

See the [MEDS-Extract documentation](https://meds-extract.readthedocs.io/) for full details on the MESSY
format.

#### `README.md`

Insert badges like below:

```markdown
[![PyPI - Version](https://img.shields.io/pypi/v/PACKAGE_NAME)](https://pypi.org/project/PACKAGE_NAME/)
[![Documentation Status](https://readthedocs.org/projects/REPO_NAME/badge/?version=latest)](https://REPO_NAME.readthedocs.io/en/stable/?badge=stable)
[![codecov](https://codecov.io/gh/Medical-Event-Data-Standard/REPO_NAME/graph/badge.svg?token=REPO_TOKEN)](https://codecov.io/gh/Medical-Event-Data-Standard/REPO_NAME)
[![tests](https://github.com/Medical-Event-Data-Standard/REPO_NAME/actions/workflows/tests.yaml/badge.svg)](https://github.com/Medical-Event-Data-Standard/REPO_NAME/actions/workflows/tests.yaml)
[![code-quality](https://github.com/Medical-Event-Data-Standard/REPO_NAME/actions/workflows/code-quality-main.yaml/badge.svg)](https://github.com/Medical-Event-Data-Standard/REPO_NAME/actions/workflows/code-quality-main.yaml)
![python](https://img.shields.io/badge/-Python_3.12-blue?logo=python&logoColor=white)
[![license](https://img.shields.io/badge/License-MIT-green.svg?labelColor=gray)](https://github.com/Medical-Event-Data-Standard/REPO_NAME#license)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Medical-Event-Data-Standard/REPO_NAME/pulls)
[![contributors](https://img.shields.io/github/contributors/Medical-Event-Data-Standard/REPO_NAME.svg)](https://github.com/Medical-Event-Data-Standard/REPO_NAME/graphs/contributors)
```

#### `tests/e2e_demo_test.py`

This test runs the full sample pipeline end-to-end — including downloading the (tiny) sample raw data —
and is enabled by default, so the template continuously verifies itself in CI.

If your dataset has an open demo version, ensure it is included in the `demo` bucket of your `sources:`
block and update the command in the `command_parts` variable to match the command you set in your
`pyproject.toml` file for the executable for your pipeline (e.g., `MIMIC-IV_extract`).

If your dataset does not have an open demo version, re-apply the `pytest.mark.skip` decorator (left
commented in the file) or remove the file, as there is no way to set up automated testing of the end-to-end
pipeline in a safe manner without a demo dataset.

The test file (and the internal doctests, which can help unittest your `pre-MEDS` file) can then be run via
`pytest --doctest-modules -s` from the root directory to ensure correctness of your pipeline. These tests will
also be run on pull requests or pushes to the `main` branch of your repository via GitHub Actions, and test
code coverage will be tracked via CodeCov.

#### `.pre-commit-config`

This will run pre-commit hooks on GitHub when you're creating your ETL. To locally install this, you can install the dev dependencies:

```bash
uv sync --group dev
```

Then, run:

```bash
uv run pre-commit run --all-files
```

This will automatically reformat your files (if possible) to conform with the linting requirements.

> \[!NOTE\]
> Currently we need pre-commit\<4 to run the `docformatter` hook.

#### `CITATION.cff`

This file ensures your resulting ETL can be properly cited. You should update the entire CFF file to reflect
your ETL; you can use the [cffinit](https://citation-file-format.github.io/cff-initializer-javascript/#/)
utility to help you.
