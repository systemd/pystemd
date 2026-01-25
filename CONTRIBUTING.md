# Contributing to pystemd
We want to make contributing to this project as easy and transparent as
possible.

## Issues
We use GitHub issues to track public bugs. Please ensure your description is
clear and has sufficient instructions to be able to reproduce the issue.

## Development setup

### Prerequisites
Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if you don't have it already:


### Installing dependencies
After cloning the repository, install the development dependencies:

```bash
uv sync --all-extras
```

### Running tests
Run the unit tests with:

```bash
uv run pytest tests
```

Or with coverage:

```bash
uv run pytest --cov=pystemd tests
```

### Running E2E tests
The E2E tests run in a systemd container using mkosi and are primarily designed
for CI. To run them locally, you need `mkosi` and `systemd-container` installed.
See `.github/workflows/e2e-tests.yml` for the full setup. For most contributions,
unit tests are sufficient.

### Formatting code
Format your code before submitting a pull request:

```bash
uv run ruff check --fix pystemd examples tests e2e
uv run ruff format pystemd examples tests e2e
uv run isort .
```

### Type checking
We use [pyrefly](https://github.com/facebook/pyrefly) for type checking. Run it with:

```bash
uv run pyrefly check pystemd examples tests
```

Optionally, you can install pre-commit hooks to automatically format code on
each commit:

```bash
uv run pre-commit install
```

## Sending a pull request
Have a fix or feature? Awesome! When you send the pull request we suggest you
include a build output.

We will hold all contributions to the same quality and style standards as the
existing code.

## License
By contributing to this repository, you agree that your contributions will be
licensed in accordance to the LICENSE document in the root of this repository.
