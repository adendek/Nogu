# NOGU
![logo.png](docs%2Fimgs%2Flogo.png)

Here will go more detailed description of what we are trying to achieve.

## Documentation

The project documentation is available [here](https://adendek.github.io/Nogu/).

The documentation contribution guide is hosted [here](/docs/README.md).

## Quick Start

### Prerequisites

- **Python 3.12+**
- **UV package manager** (recommended) or pip

### Quick Installation

```bash
# Clone the repository
git clone <repository-url>
cd nogu

# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync
```

## Installation

### Using UV (Recommended)

The project uses [UV](https://github.com/astral-sh/uv) for fast dependency management:

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies (including dev dependencies)
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

### Using pip

If you prefer using pip:

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -e .
```

### Verify Installation

```bash
# Check Python version (should be 3.10+)
python --version

# Verify key dependencies
python -c " import torch; print('Dependencies OK')"
```

## Testing

### Running Tests

Tests must be run using `uv run` to ensure the correct environment:

```bash
# Run unit tests (excludes E2E tests)
uv run pytest -k "not e2e"

# Run End-to-End (E2E) tests
uv run pytest -k "e2e"

# Run with coverage report
uv run pytest --cov=nogu --cov-report=term-missing

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/UT/test_orchestrator.py

# Run tests with print statements visible
uv run pytest -s
```

### Test Configuration

The project uses `pytest` with the following configuration (from `pyproject.toml`):

- **Coverage**: Enabled with XML and terminal reports
- **JUnit XML**: Test results exported to `testresults.xml`
- **Coverage Reports**: Generated in `coverage.xml`

### Test Structure

```
tests/
├── UT/              # Unit tests
└── E2E/             # End-to-end tests
```


### Code Style

The project follows these conventions:

- **PEP 8**: Python style guide
- **Type Hints**: Extensive use of type hints in function signatures
- **Docstrings**: Google-style docstrings for public methods
- **Ruff**: Code formatting and linting (configured in `pyproject.toml`)

### Running Code Quality Checks

Code quality checks are executed using `pre-commits`

```bash
 uv run  pre-commit run --all-file
```

### Creating a Jupyter Kernel

To create a Jupyter kernel for your project:

```bash
uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=writeoffs
```
This allows you to select the project-specific kernel in Jupyter notebooks.

### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** and test locally:
   ```bash
   uv run pytest
   uv run ruff check oee/
   ```

3. **Commit changes** following [Conventional Commits](https://www.conventionalcommits.org/):
   ```bash
   git commit -m "feat: add new feature"
   ```

4. **Push and create Pull Request**

### Project-Specific Conventions

1. **Module Organization**: The project follows hexagonal architecture with core logic in `_src/` directory
2. **Type Hints**: Extensive use of Python type hints throughout the codebase
3. **Pydantic Models**: All API request/response models and internal data structures use Pydantic for validation
4. **Logging**: Loguru is used for structured logging with appropriate log levels
5. **Async Processing**: Long-running tasks are executed as background tasks to keep API responsive
6. **Artifact Naming**: Artifacts use `.art` extension for pickled models and `.parquet` for data files


## Additional Documentation
### Project Documentation

- [Project Documentation Index](./docs/index.md)
- [Jupyter Notebooks for Analysis](./notebooks/)

---

**Note**: This README provides essential information for getting started, running, and deploying the application. For detailed architectural information and in-depth analysis, refer to the documentation in the `docs/` directory.
