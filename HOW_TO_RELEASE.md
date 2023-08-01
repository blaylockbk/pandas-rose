# How to release `pandas-rose`

## Create a release

In VS Code:

1. Commit and push all changes.
1. Make sure HEAD is where you want to be (the latest commit on main branch)
1. `Git: Create Tag` and specify tag `YYYY.M.micro` and a message.
1. `Git: Push Tags`

In GitHub

1. Let GitHub actions build and publish the tag to PyPI.
1. On GitHub.com, draft a new release with the specified tag, write some release notes, and finish.

## Build the package locally

```
python -m build
```
