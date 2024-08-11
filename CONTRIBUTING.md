# Contributing Guide

Thank you for taking your time in contributing to this project.  Any
contribution made to the code will be acknowledged in our
[change log](CHANGELOG.md).  Please read this guide fully before
submitting any changes or issues to the project.

## Table of Contents

1. [Getting Started](#getting-started)
1. [Branching Model](#branching-model)
1. [Submitting Changes](#submitting-changes)
1. [Code Review](#code-review)
1. [Guidelines](#guidelines)
   - [Commit Messages](#commit-messages)
1. [Issues and Bugs](#issues-and-bugs)
1. [Documentation](#documentation)
1. [Maintainers Only](#maintainers-only)
   - [Cutting a New Release](#cutting-a-new-release)

## Getting Started

To run the end-to-end tests locally for this project, you will need a Python
environment and Docker installed.  In these examples, we use
[pyenv](https://github.com/pyenv/pyenv).  We also have a bias towards
*NIX/Mac for development platforms, but may look at migrating to a
[Dev Container](https://code.visualstudio.com/docs/devcontainers/containers)
configuration.

1. Fork the repository from <https://github.com/cbdq-io/a-fake-rotor-true/fork>.
1. Clone your fork (using either HTTPS or SSH):
   ```shell
   # Using HTTPS
   git clone https://github.com/YOUR_USERNAME/a-fake-rotor-true.git

   # Using SSH
   git clone git@github.com:YOUR_USERNAME/a-fake-rotor-true.git
   ```
1. Setup the Upstream Repository
   ```shell
   cd a-fake-rotor-true

   # If using HTTP
   git remote add upstream https://github.com/cbdq-io/a-fake-rotor-true.git

   # If using SSH
   git remote add upstream git@github.com:cbdq-io/a-fake-rotor-true.git
   ```
1. Setup the PyEnv Environment
   ```shell
   pyenv virtualenv a-fake-rotor-true
   pyenv local a-fake-rotor-true
   pip install -Ur requirements.txt requirements-dev.txt
   ```
1. Run End-to-End Tests
   ```shell
   make
   ```

## Branching Model

We use the
[Gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
branching model.  Here's the summary:

1. **Main branches**:
   - `main`:  The stable production branch.
   - `develop`:  The integration branch for new features and bugfixes.
2. **Supported branches**:
   - `feature/*`:  For developing new features.  Branch off from `develop`.
   - `bugfix/*`:  For developing new bug fixes.  Branch off from `develop`.
   - `release/*`:  For preparing a new release.  Branch off from `develop`.
     Used by maintainers only.
   - `hotfix/*`:  For urgent fixes on the production code.  Branch off
     from `main`.  Used by maintainers only.

   If we need to support legacy versions, then there are also
   `support/*` branches as well.

### Creating a Branch

1. Feature Branch:
   ```shell
   git checkout develop
   git pull upstream develop
   git checkout -b feature/your-feature-name
   ```
1. Bugfix Branch:
   ```shell
   git checkout develop
   git pull upstream develop
   git checkout -b bugfix/your-bugfix-name
   ```

## Submitting Changes

1. Commit your changes:
   Please ensure that your commit messages follow our
   [commit message](#commit-messages) guidelines.
   ```bash
   git add .
   git commit -m 'Your commit message.'
   ```
2. Push your branch:
   ```shell
   # For a feature branch.
   git push origin feature/your-feature-name

   # For a bugfix branch.
   git push origin bugfix/your-bugfix-name
   ```
3. Create a Pull Request:
	- Navigate to your forked repository on GitHub.
	- Click the “Compare & pull request” button.
	- Select develop as the base branch and your branch as the compare branch.
	- Provide a clear description of your changes.

## Code Review

- Your pull request will be reviewed by the maintainers.
- Address any feedback and make necessary changes.
- Once approved, your changes will be merged.

## Guidelines

- Follow the coding standards established in the project.
- Write meaningful commit messages.  More on that below.
- Ensure that your code is well-documented.
- Write tests for new features or changes.


### Commit Messages

[Change logs](CHANGELOG.md) are useful, but it's a schlep maintaining them.
To reduce the pain, we use the
[Git Change Log](https://pypi.org/project/gitchangelog/) packages that
uses the Git history to generate the change log (in this project, the
change log is generated automatically as part of the pull request
process).

For each release (which is calculated from Git tags), the following sections
are available:

- New: For new additions or features to the project.
- Changes: For changes that have been introduced.
- Fix: For any fixes that have been carried out during this release.
- Other: Where no category has been able to be guessed from the commit
  message.

To ensure your well-crafted, meaningful commit message is properly
directed to the correct section, prefix it with the appropriate keyword
for the correct section.

Here are some use cases to describe getting your commit message to
the correct section:

- Adding a new feature:
  ```shell
  git commit -m 'new: Add feature X.'
  ```
- Recording a Change:
  ```shell
  git commit -m 'chg: Bump base image from 1.1.2 to 1.2.0.'
  ```
- Recording a Fix:
  ```shell
  git commit -m 'fix: Correct main parameter names.`
  ```
- Commit a minor change that you don't want recorded in the change log:
  ```shell
  git commit -m 'fix: dev: Fix bad YAML syntax error.'
  ```

Any commit message with out the new, chg or fix prefixes that are not also
prefixed with `fix: dev:` will be added to the _Other_ section of the change
log.

## Issues and Bugs

- Check the existing
  [issues](https://github.com/cbdq-io/a-fake-rotor-true/issues) before
  submitting a new one.
- If you find a bug, please open an issue with a clear description and steps to reproduce.

## Documentation

- Update the documentation for any new features or changes you make.
- Ensure that the documentation is clear and concise.

## Maintainers Only

This section is for information that only applies to the maintainers of this
repository.

### Cutting a New Release

1. Creating a Release Branch:
   ```shell
   git checkout develop
   git pull
   git checkout -b release/your-release-name
   ```

   Now edit `router.py` and ensure that `__version__` is set to the same
   as the proposed release name.
2. Run the local end-to-end tests:
   ```shell
   make
   ```
   Only progress to the next step when all tests pass.
3. Push the release branch:
   ```shell
   git push origin release/your-release-name
   ```
4. Create a pull request to merge the release branch onto `main`.
