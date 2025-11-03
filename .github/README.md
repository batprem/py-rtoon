# GitHub Workflows Documentation

This directory contains GitHub Actions workflows for CI/CD automation.

## Workflows

### 1. CI Workflow (`ci.yml`)

**Trigger:** Push to main, Pull Requests

**Purpose:** Continuous integration testing

**Jobs:**
- **test**: Runs tests on multiple platforms and Python versions
  - OS: Ubuntu, macOS, Windows
  - Python: 3.9, 3.10, 3.11, 3.12, 3.13
  - Steps: Build extension, run pytest

- **build**: Builds wheels to verify they can be created
  - Runs on all platforms
  - Uses maturin-action for building

**Status:** [![CI](https://github.com/premchotipanit/py-rtoon/actions/workflows/ci.yml/badge.svg)](https://github.com/premchotipanit/py-rtoon/actions/workflows/ci.yml)

### 2. Test Workflow (`test.yml`)

**Trigger:** Push to main/develop, Pull Requests

**Purpose:** Comprehensive testing with linting

**Jobs:**
- **test**: Full test matrix (same as CI)
- **lint**: Code quality checks with ruff

### 3. Publish Workflow (`publish.yml`)

**Trigger:** GitHub Releases, Manual dispatch

**Purpose:** Automated publishing to PyPI

**Jobs:**

1. **linux**: Build Linux wheels (x86_64, aarch64)
2. **windows**: Build Windows wheels (x64)
3. **macos**: Build macOS wheels (x86_64, aarch64)
4. **sdist**: Build source distribution
5. **release**: Upload all distributions to PyPI

**Features:**
- Builds for Python 3.9-3.13
- Multi-platform support
- Uses trusted publishing (OIDC)
- Automatic artifact collection
- Caches build with sccache

## Setup Required

### For Trusted Publishing (Recommended)

1. **PyPI Setup:**
   - Register pending publisher on PyPI
   - Project: `py-rtoon`
   - Workflow: `publish.yml`
   - Environment: `pypi`

2. **GitHub Setup:**
   - Create environment named `pypi`
   - (Optional) Add protection rules

See [PYPI_SETUP.md](PYPI_SETUP.md) for detailed instructions.

### For API Token (Alternative)

1. Generate PyPI API token
2. Add to GitHub Secrets as `PYPI_API_TOKEN`
3. Update publish workflow to use token

## Usage

### Running Tests Locally

```bash
# Run all tests
uv run pytest

# Run on specific Python version
python3.9 -m pytest
python3.13 -m pytest
```

### Building Locally

```bash
# Build wheel
uv run maturin build --release

# Build and install locally
uv run maturin develop --release
```

### Testing Build

```bash
# Run test script
./scripts/test_build.sh
```

### Creating a Release

1. Update version in `pyproject.toml`
2. Commit and tag:
   ```bash
   git add pyproject.toml
   git commit -m "Bump version to 0.2.0"
   git tag v0.2.0
   git push origin main --tags
   ```
3. Create GitHub Release
4. Workflow automatically publishes to PyPI

## Workflow Files

```
.github/
├── workflows/
│   ├── ci.yml          # Main CI workflow
│   ├── test.yml        # Extended testing
│   └── publish.yml     # PyPI publishing
├── PYPI_SETUP.md       # PyPI setup guide
└── README.md           # This file
```

## Troubleshooting

### Tests Failing

1. Check test output in Actions tab
2. Run tests locally: `uv run pytest -v`
3. Verify Rust compiles: `cargo build --release`

### Build Failing

1. Check maturin version compatibility
2. Verify Rust toolchain is up to date
3. Check platform-specific dependencies

### Publish Failing

1. Verify trusted publishing setup on PyPI
2. Check workflow permissions (`id-token: write`)
3. Ensure version number is unique
4. Verify environment name matches (`pypi`)

## Monitoring

- **CI Status:** Monitor via GitHub Actions tab
- **PyPI Stats:** View on [PyPI project page](https://pypi.org/project/py-rtoon/)
- **Download Stats:** Use [pypistats.org](https://pypistats.org/packages/py-rtoon)

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyO3/maturin-action](https://github.com/PyO3/maturin-action)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [Maturin Guide](https://www.maturin.rs/)
