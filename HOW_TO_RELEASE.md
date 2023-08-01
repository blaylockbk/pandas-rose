# How to release `pandas-rose`


## Build the package locally

```
python -m build
```


## Create a release
In VS Code, 

- commit and push all changes
- `Git: Create Tag` and specify tag `YYYY.M.micro` and a message.
- `Git: Push Tags`
- Let GitHub actions publish the tag to PyPI and create a GitHub release.
- Edit the GitHub release page with CHANGELOG info.
