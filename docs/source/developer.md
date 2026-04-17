# Developer Instructions

Guidance for core developers

## Management of Requirements
Requirements of the project should be added to `requirements.txt` and `conda_recipe/meta.yaml`.
Use [edgetest](https://github.com/capitalone/edgetest) to determine when pins need to change.
```
pip install -e .[dev]
edgetest -c pyproject.toml
```

## Release Process
Increase the package version using `bumpversion`.
```
bumpversion minor
git add --all
git commit -m "Updated +semver: minor"
```
bumpversion expects `minor`, `major`, or `patch` as release types and will update the version as `major.minor.patch`.
**Note:** bumpversion gets confused by multiple commits with different indications, e.g., `major` and `minor`, so do this as the last step and do it once.
bumpversion works when dev requirements are installed.

## PIP Packaging
```
conda create -n pip_package python=3.9 -y
conda activate pip_package
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*
```

## Conda Packaging
See `build_conda.sh`.
