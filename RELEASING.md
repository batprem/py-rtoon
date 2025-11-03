# Release Process for py-rtoon

This document describes how to release py-rtoon to PyPI.

## Prerequisites

1. **PyPI Account Setup**
   - Create an account on [PyPI](https://pypi.org/)
   - Create an account on [TestPyPI](https://test.pypi.org/) for testing

2. **GitHub Repository Setup**
   - Enable trusted publishing on PyPI (recommended) or set up API token
   - Configure GitHub repository secrets if using API tokens

## Automated Release (Recommended)

The project uses GitHub Actions for automated releases. The workflow builds wheels for multiple platforms and Python versions automatically.

### Step 1: Update Version

Update the version in `pyproject.toml`:

```toml
[project]
name = "py-rtoon"
version = "0.2.0"  # Update this
```

### Step 2: Update Changelog

Document changes in the release notes.

### Step 3: Commit and Tag

```bash
git add pyproject.toml
git commit -m "Bump version to 0.2.0"
git tag v0.2.0
git push origin main --tags
```

### Step 4: Create GitHub Release

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Select the tag you just created (v0.2.0)
4. Write release notes
5. Click "Publish release"

**The GitHub Action will automatically:**
- Build wheels for Linux (x86_64, aarch64)
- Build wheels for macOS (x86_64, aarch64/Apple Silicon)
- Build wheels for Windows (x64)
- Build source distribution (sdist)
- Upload all distributions to PyPI

## Trusted Publishing Setup (Recommended)

Trusted publishing is the most secure method and doesn't require storing API tokens.

### On PyPI

1. Go to your PyPI account settings
2. Navigate to "Publishing" → "Add a new pending publisher"
3. Fill in:
   - PyPI Project Name: `py-rtoon`
   - Owner: `your-github-username`
   - Repository name: `py-rtoon`
   - Workflow name: `publish.yml`
   - Environment name: `pypi`

### In GitHub Repository

1. Go to repository Settings → Environments
2. Create a new environment named `pypi`
3. (Optional) Add protection rules requiring reviewers

## Manual Release (Alternative)

If you need to release manually:

### Install Build Tools

```bash
uv add --dev maturin build twine
```

### Build Distributions

```bash
# Build wheels
uv run maturin build --release

# Or build source distribution
uv run maturin sdist
```

### Test on TestPyPI

```bash
# Upload to TestPyPI
uv run twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ py-rtoon
```

### Upload to PyPI

```bash
# Upload to PyPI
uv run twine upload dist/*
```

## Verification

After release, verify the package:

```bash
# Install from PyPI
pip install py-rtoon

# Test basic functionality
python -c "import py_rtoon; print(py_rtoon.__version__)"

# Run a quick test
python -c "
import py_rtoon
import json
data = {'test': 'value'}
toon = py_rtoon.encode_default(json.dumps(data))
print('Success:', toon)
"
```

## Multi-platform Wheels

The GitHub Action builds wheels for:

**Linux:**
- x86_64 (Intel/AMD)
- aarch64 (ARM)

**macOS:**
- x86_64 (Intel)
- aarch64 (Apple Silicon M1/M2/M3)

**Windows:**
- x64 (Intel/AMD)

**Python Versions:**
- 3.9, 3.10, 3.11, 3.12, 3.13

## Troubleshooting

### Build Failures

If builds fail in GitHub Actions:

1. Check the Actions tab for error messages
2. Verify Rust code compiles locally: `cargo build --release`
3. Verify Python tests pass: `uv run pytest`
4. Check that all platforms are configured correctly

### PyPI Upload Failures

If PyPI upload fails:

1. Verify trusted publishing is configured correctly
2. Check that the version number is unique (not already on PyPI)
3. Ensure all required metadata is in `pyproject.toml`
4. Verify the workflow has `id-token: write` permission

### Missing Wheels

If some platform wheels are missing:

1. Check if that platform's job failed in Actions
2. Verify the maturin-action supports that platform
3. Check Rust dependencies are compatible with all platforms

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0): Incompatible API changes
- **MINOR** (0.1.0): Backwards-compatible functionality
- **PATCH** (0.0.1): Backwards-compatible bug fixes

## Pre-release Versions

For pre-releases, use suffixes:

- Alpha: `0.2.0a1`
- Beta: `0.2.0b1`
- Release Candidate: `0.2.0rc1`

Example:

```toml
version = "0.2.0b1"
```

Tag as: `v0.2.0b1`

## Rollback

If you need to yank a release:

1. Go to PyPI project page
2. Click on the version to yank
3. Click "Options" → "Yank release"
4. Provide a reason

**Note:** Yanking doesn't delete the release, it just prevents new installations.

## Checklist

Before releasing:

- [ ] All tests pass (`uv run pytest`)
- [ ] Version bumped in `pyproject.toml`
- [ ] Changelog updated
- [ ] README.md is up to date
- [ ] All changes committed and pushed
- [ ] Tag created and pushed
- [ ] GitHub release created
- [ ] Verified installation from PyPI
- [ ] Documentation is accurate

## Resources

- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [Maturin Documentation](https://www.maturin.rs/)
- [PyO3 Maturin Action](https://github.com/PyO3/maturin-action)
- [Python Packaging Guide](https://packaging.python.org/)
