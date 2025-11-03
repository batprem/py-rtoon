# GitHub Workflows Configuration

## Path Filters

All CI workflows are configured to skip running when only documentation files are changed, saving CI/CD resources and reducing carbon footprint.

### Ignored Paths

The following paths are ignored by CI workflows:

- `**.md` - All markdown files (README, docs, etc.)
- `docs/**` - Documentation directory
- `.gitignore` - Git ignore file
- `LICENSE` - License file

### Why Skip Documentation Changes?

Documentation-only changes don't affect:
- Code functionality
- Test results
- Build artifacts
- Package distribution

Skipping these saves:
- ⏱️ CI/CD time (~15-30 minutes per workflow run)
- 💰 GitHub Actions minutes (especially for private repos)
- 🌱 Energy and carbon emissions
- 📊 Cleaner workflow history

## Workflow Triggers

### ci.yml
**Runs on:**
- Push to `main` branch (excluding docs)
- Pull requests (excluding docs)

**Purpose:**
- Test on multiple platforms (Ubuntu, macOS, Windows)
- Test on multiple Python versions (3.9-3.13)
- Build wheels to verify compilation

### test.yml
**Runs on:**
- Push to `main` or `develop` branches (excluding docs)
- Pull requests to `main` or `develop` (excluding docs)

**Purpose:**
- Comprehensive testing
- Code linting with ruff
- Type checking (Python 3.11+)

### publish.yml
**Runs on:**
- GitHub releases (published)
- Manual workflow dispatch

**Purpose:**
- Build multi-platform wheels
- Build source distribution
- Publish to PyPI

**Note:** This workflow does NOT have path filters because:
- Only runs on releases (not push events)
- Documentation updates don't trigger releases
- Manual dispatch is intentional

## Examples

### Will Trigger CI
```bash
# Code changes
git commit -m "Fix bug in encoding"
git commit -m "Add new feature"
git commit -m "Update dependencies"

# Test changes
git commit -m "Add test coverage"

# Workflow changes
git commit -m "Update CI configuration"
```

### Will NOT Trigger CI
```bash
# Documentation only
git commit -m "Update README"
git commit -m "Fix typo in docs"
git commit -m "Add examples to README.md"

# Mixed changes - WILL STILL RUN if any code files changed
git commit -m "Update README and fix bug"  # ← Runs because of bug fix
```

## Testing Path Filters

To verify path filters are working:

1. Make a documentation-only change:
   ```bash
   echo "# Test" >> README.md
   git add README.md
   git commit -m "docs: test CI skip"
   git push
   ```

2. Check GitHub Actions tab - workflow should be skipped
3. Look for: "Workflow run was skipped"

## Overriding Path Filters

If you need to run CI on documentation changes:

### Option 1: Empty commit
```bash
git commit --allow-empty -m "Trigger CI [ci run]"
```

### Option 2: Touch a code file
```bash
touch src/py_rtoon/__init__.py
git add src/py_rtoon/__init__.py
git commit -m "docs: update README [trigger CI]"
```

### Option 3: Manual dispatch
- Go to Actions tab
- Select workflow
- Click "Run workflow"

## Best Practices

### Commit Message Conventions

Use conventional commits to indicate change type:

```bash
git commit -m "docs: update README"        # Documentation
git commit -m "feat: add dict encoding"    # Feature
git commit -m "fix: resolve decoding bug"  # Bug fix
git commit -m "test: add edge cases"       # Tests
git commit -m "chore: update dependencies" # Maintenance
```

### Separate Documentation PRs

For documentation-heavy work:

1. Create dedicated documentation PR
2. CI won't run (faster review)
3. Merge without waiting for builds

For mixed changes:

1. Keep code and docs together
2. CI will run normally
3. Ensures code changes are tested

## Monitoring

Track workflow efficiency:

- Check Actions tab for skipped runs
- Monitor "Workflow run was skipped" messages
- Review time saved over weeks/months

Example savings (per skipped run):
- CI workflow: ~20 minutes
- Test workflow: ~25 minutes
- Total: ~45 minutes per documentation commit

If you commit docs 3x/week:
- **~135 minutes/week saved**
- **~540 minutes/month saved**
- **~9 hours/month saved**

## Resources

- [GitHub Actions Path Filters](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onpushpull_requestpull_request_targetpathspaths-ignore)
- [Conventional Commits](https://www.conventionalcommits.org/)
