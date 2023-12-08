# Blue Book

In this page our coding guidelines, building processes, version control practices are explained.

## Building tools

In the Python projects, we use `poetry` as our building tool. It handles our dependencies and our build/deploy steps.

All the configuration data must be in the `pyproject.toml` file.

## Coding guidelines

Readability counts!

When coding in Python, we comply with the [PEP8](https://pep8.org/) (or [official PEP8](https://peps.python.org/pep-0008/)) rules.

### Formatting

Our code is also formatted by [`black`](https://black.readthedocs.io/en/stable/index.html) and `isort`, with Blacks default maximum line length of **88** characters.

Note: the formatting happens via `ruff`, which is a rust implementation the `black`/`isort`. 

### Linting

Our code is linted at each commit/push and by our ci/cd. The linters are part of the `pre-commit` structure. Things like a too high code complexity, remaining `print` statements, misuse of f-strings,... are spotted. 

Note: the lining happens via `ruff`, which is a rust implementation of flake8 and many of its plugins.  [These rules](https://docs.astral.sh/ruff/rules/) are checked.

The `tests` directory is not linted.

### Tests

We use `pytest` as test tool.  We create a coverage report for each run.

## Commit rules

We use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) (and therefor [semantic versioning](https://semver.org/)).

We also strive to use the semantic release process, which will make our release management much smoother.  See [Python semantic release](https://semantic-release.gitbook.io/semantic-release/) for more information.

All the formatters and linters must be run locally first (before commiting), but also will be run by the ci/cd.

## Branching strategy

We will use a [truck based](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development) development.

So we keep the work on our branches short and simple, have few (less than three) active branches, we use feature flags to enable/disable features or services. 

We merge often, using a test system witch enabled coverage report and other analytics.

We strive to have a ticket identifier in our branches (e.g. `add_verbosity_level_to_runbook_#8023`)

## Documentation

Documentation must be part of our code, so it should be part of its repo.

## Code review rules

The pull request must be reviewed by the repository owner.
