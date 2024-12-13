# Extract your custom dataset via MEDS-Transforms

[![codecov](https://codecov.io/gh/mmcdermott/ETL_MEDS_Template/graph/badge.svg?token=RW6JXHNT0W)](https://codecov.io/gh/mmcdermott/ETL_MEDS_Template)
[![tests](https://github.com/mmcdermott/ETL_MEDS_Template/actions/workflows/tests.yaml/badge.svg)](https://github.com/mmcdermott/ETL_MEDS_Template/actions/workflows/tests.yml)
[![code-quality](https://github.com/mmcdermott/ETL_MEDS_Template/actions/workflows/code-quality-main.yaml/badge.svg)](https://github.com/mmcdermott/ETL_MEDS_Template/actions/workflows/code-quality-main.yaml)
![python](https://img.shields.io/badge/-Python_3.12-blue?logo=python&logoColor=white)
[![license](https://img.shields.io/badge/License-MIT-green.svg?labelColor=gray)](https://github.com/mmcdermott/ETL_MEDS_Template#license)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/mmcdermott/ETL_MEDS_Template/pulls)
[![contributors](https://img.shields.io/github/contributors/mmcdermott/ETL_MEDS_Template.svg)](https://github.com/mmcdermott/ETL_MEDS_Template/graphs/contributors)

A template repository for a MEDS-Transforms powered extraction pipeline for a custom dataset.

## How to use this repository

1. Initialize a new repository using this template repository.
2. Customize the following code points:

- [`src/.../dataset.yaml`](todo)

1. Customize the following external services:

- CodeCov
- PyPI

### Code Points:

#### `dataset.yaml`

#### `event_configs.yaml`

#### `pre_MEDS.py`

#### `download`

#### `README.md`

Insert badges like below:

```markdown
[![PyPI - Version](https://img.shields.io/pypi/v/PACKAGE_NAME)](https://pypi.org/project/PACKAGE_NAME/)
[![Documentation Status](https://readthedocs.org/projects/REPO_NAME/badge/?version=latest)](https://REPO_NAME.readthedocs.io/en/stable/?badge=stable)
[![codecov](https://codecov.io/gh/mmcdermott/REPO_NAME/graph/badge.svg?token=REPO_TOKEN)](https://codecov.io/gh/mmcdermott/REPO_NAME)
[![tests](https://github.com/mmcdermott/REPO_NAME/actions/workflows/tests.yaml/badge.svg)](https://github.com/mmcdermott/REPO_NAME/actions/workflows/tests.yml)
[![code-quality](https://github.com/mmcdermott/REPO_NAME/actions/workflows/code-quality-main.yaml/badge.svg)](https://github.com/mmcdermott/REPO_NAME/actions/workflows/code-quality-main.yaml)
![python](https://img.shields.io/badge/-Python_3.12-blue?logo=python&logoColor=white)
[![license](https://img.shields.io/badge/License-MIT-green.svg?labelColor=gray)](https://github.com/mmcdermott/REPO_NAME#license)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/mmcdermott/REPO_NAME/pulls)
[![contributors](https://img.shields.io/github/contributors/mmcdermott/REPO_NAME.svg)](https://github.com/mmcdermott/REPO_NAME/graphs/contributors)
```

#### `pyproject.toml`

### External Services

#### CodeCov

1. Go to [CodeCov](https://codecov.io/) and add make an account or log-in as needed.
2. Follow the instructions to configure your new repository with CodeCov.
3. Copy the badge markdown from CodeCov and paste it into the `README.md` file. To find the badge markdown
    link, go to your repository in CodeCov, click on the "Configuration" tab, click on the "Badges and
    Graphs" option, then copy the markdown link from the top section and paste it in the corresponding line
    of the README, in place of the default link included above.
4. It will now track the test coverage of your ETL, including running the full pipeline against the linked
    demo data you provide in `dataset.yaml`.

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
![PyPI Trusted Publisher](<>)
