# Contributing to JobJourney

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:
- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features

## We Develop with Github
We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Branch Policy
- The `master` branch should always be in a deployable state and is automatically deployed to the staging environment on each new commit.
- We do **not** follow GitFlow; there is no `dev` branch.
- All work is done in short-lived feature branches that are merged into `master` once they have been tested and approved.

## Contribution Workflow
1. Fork the repo and create your branch from `master`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes and your code lints.
4. Squash your commits and ensure your commit messages are meaningful.
5. Submit your pull request.

## Keeping Commit History Linear
- **Only fast-forward merges are allowed**. Our repository has been set up to support this, ensuring a linear commit history.
- **Squashing Commits**: Before merging, ensure commits are squashed. Each commit should represent a well-tested product increment. PRs should usually have only one commit.
- **Commit Messages**: Write meaningful commit messages, prefacing them with the ticket number in square brackets (e.g., `[123] Add new feature`).

## Squashing and Rebasing Instructions
- Fetch the latest changes from GitHub:
  ```
  git fetch origin
  ```
- Rebase your branch on top of `master` and squash multiple commits:
  ```
  git rebase -i origin/master
  ```
- Update the remote branch on GitHub:
  ```
  git push -f origin <my_branch>
  ```
- Merge your branch to `master`. This is only allowed if your branch is rebased on top of `master` and the PR has been approved. It also merges the PR and deletes the feature branch on GitHub:
  ```
  git push origin <my_branch>:master
  ```

## Reporting Bugs
Use GitHub issues to report bugs. Provide detailed reports with reproducible steps, expected outcomes, and actual outcomes.

## License
By contributing, you agree that your contributions will be licensed under its [MIT License](https://github.com/ArgDevs/JobJourney/LICENSE.md).

## References
This document was adapted from open-source contribution guidelines such as [Facebook's Draft](https://github.com/facebook/draft-js/blob/master/CONTRIBUTING.md).
