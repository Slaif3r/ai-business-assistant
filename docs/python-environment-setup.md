# Python Environment Setup Guide

This guide explains how to set up and manage Python environments for this project to avoid version conflicts.

## 🎯 Multi-Layer Protection Against Version Conflicts

This project uses **4 layers** of version control:

### 1. **Python Version Pinning** (`.python-version`)
- Specifies exact Python version: **3.11.7**
- Used by `pyenv` to automatically switch versions
- Ensures everyone uses the same Python version

### 2. **Dependency Constraints** (`pyproject.toml`)
- Modern Python project configuration
- Defines version ranges for dependencies
- Separates dev, ML, viz, and notebook dependencies

### 3. **Exact Version Locking** (`requirements.txt`)
- Pins exact versions that work together
- Generated from `pip freeze` after testing
- Ensures reproducible builds

### 4. **Virtual Environments**
- Isolates project dependencies
- Prevents conflicts with system packages
- Automatically created in Docker container

---

## 🚀 Quick Start

### Inside Docker Container (Recommended)

The Docker container automatically:
- ✅ Installs Python 3.11
- ✅ Creates a virtual environment at `/home/builduser/.venv`
- ✅ Activates the virtual environment
- ✅ Installs dependencies from `requirements.txt`

**Just start the container and you're ready!**

```bash
cd .devcontainer
docker-compose up -d
```

### On Your Local Machine (Optional)

If you want to develop outside Docker:

#### 1. Install pyenv (if not already installed)

**macOS:**
```bash
brew install pyenv
```

**Linux:**
```bash
curl https://pyenv.run | bash
```

#### 2. Install Python 3.11.7

```bash
pyenv install 3.11.7
pyenv local 3.11.7  # Uses .python-version file
```

#### 3. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

#### 4. Install Dependencies

```bash
# Core dependencies
pip install -r requirements.txt

# Development dependencies
pip install -r requirements-dev.txt

# Or install everything from pyproject.toml
pip install -e ".[all]"
```

---

## 📦 Dependency Management

### Adding New Dependencies

1. **Add to `pyproject.toml`** with version constraint:
   ```toml
   dependencies = [
       "new-package>=1.0.0,<2.0.0",
   ]
   ```

2. **Install and test:**
   ```bash
   pip install -e .
   ```

3. **Update `requirements.txt`** with exact version:
   ```bash
   pip freeze | grep new-package >> requirements.txt
   ```

### Updating Dependencies

```bash
# Update a specific package
pip install --upgrade package-name

# Regenerate requirements.txt
pip freeze > requirements.txt
```

### Different Dependency Sets

```bash
# Development tools
pip install -e ".[dev]"

# Machine learning
pip install -e ".[ml]"

# Data visualization
pip install -e ".[viz]"

# Jupyter notebooks
pip install -e ".[notebook]"

# Everything
pip install -e ".[all]"
```

---

## 🛡️ Code Quality Tools

### Pre-commit Hooks (Automated)

Automatically run checks before each commit:

```bash
# Install pre-commit hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

**What it checks:**
- ✅ Code formatting (Black)
- ✅ Import sorting (isort)
- ✅ Linting (flake8)
- ✅ Type checking (mypy)
- ✅ Security issues (bandit)
- ✅ File issues (trailing whitespace, etc.)

### Manual Code Quality Checks

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 src/

# Type check
mypy src/

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html
```

---

## 🔍 Troubleshooting

### "Wrong Python version"

```bash
# Check current version
python --version

# Should show: Python 3.11.7

# If not, activate virtual environment
source .venv/bin/activate
```

### "Module not found"

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or reinstall in editable mode
pip install -e .
```

### "Dependency conflict"

```bash
# Create fresh virtual environment
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### "Pre-commit hooks failing"

```bash
# Update hooks
pre-commit autoupdate

# Clear cache and retry
pre-commit clean
pre-commit run --all-files
```

---

## 📊 Project Structure

```
ai-business-assistant/
├── .python-version          # Python version (3.11.7)
├── pyproject.toml           # Project config & dependencies
├── requirements.txt         # Pinned core dependencies
├── requirements-dev.txt     # Pinned dev dependencies
├── .pre-commit-config.yaml  # Code quality automation
├── .venv/                   # Virtual environment (local)
├── src/                     # Source code
│   └── __init__.py
└── tests/                   # Test files
```

---

## 🎓 Best Practices

1. **Always use virtual environments** - Never install packages globally
2. **Pin versions in requirements.txt** - Use exact versions for reproducibility
3. **Use version ranges in pyproject.toml** - Allow compatible updates
4. **Run pre-commit hooks** - Catch issues before committing
5. **Test after updates** - Always test after updating dependencies
6. **Document changes** - Update requirements files when adding packages

---

## 🔗 Related Files

- [pyproject.toml](file:///home/builduser/APP/ai-business-assistant/pyproject.toml) - Project configuration
- [requirements.txt](file:///home/builduser/APP/ai-business-assistant/requirements.txt) - Core dependencies
- [requirements-dev.txt](file:///home/builduser/APP/ai-business-assistant/requirements-dev.txt) - Dev dependencies
- [.pre-commit-config.yaml](file:///home/builduser/APP/ai-business-assistant/.pre-commit-config.yaml) - Code quality hooks
- [Dockerfile.dev](file:///home/builduser/APP/ai-business-assistant/docker/Dockerfile.dev) - Docker Python setup
