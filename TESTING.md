# Personal Website - Testing Guide

This Flask-based personal website includes comprehensive testing to ensure reliability and maintainability.

## 🧪 Test Structure

### Test Files
- **`test_database.py`** - Tests the Data Access Layer (DAL) functionality
- **`test_projects.py`** - Tests Flask routes and application functionality
- **`run_tests.py`** - Convenient test runner script
- **`pytest.ini`** - Pytest configuration

### Test Coverage
- **Database Operations**: 100% coverage
- **Flask Routes**: 100% coverage  
- **Overall Coverage**: 99% (395/397 statements)

## 🚀 Running Tests

### Quick Commands

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run without warnings
python -m pytest --disable-warnings

# Run with coverage report
python -m pytest --cov=. --cov-report=html
```

### Using the Test Runner Script

```bash
# Run all tests
python run_tests.py

# Run only database tests
python run_tests.py --type=db

# Run only Flask tests  
python run_tests.py --type=flask

# Run with coverage
python run_tests.py --type=coverage

# Suppress warnings
python run_tests.py --no-warnings

# Verbose output
python run_tests.py --verbose
```

## 📋 Test Categories

### Database Tests (`test_database.py`)
- ✅ Database initialization and table creation
- ✅ Data seeding and idempotency
- ✅ CRUD operations (Create, Read, Update, Delete)
- ✅ Slug generation and uniqueness
- ✅ Connection handling and cleanup
- ✅ Error handling for edge cases

### Flask Application Tests (`test_projects.py`)
- ✅ All route functionality (home, about, resume, projects, etc.)
- ✅ Project page rendering with database data
- ✅ Form submission and validation
- ✅ File upload handling
- ✅ Static file serving
- ✅ Navigation and links
- ✅ Error pages (404)
- ✅ Client-side form validation

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)
```ini
[tool:pytest]
testpaths = .
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### Test Dependencies (`requirements.txt`)
```
pytest==7.4.3
pytest-flask==1.3.0
pytest-cov==4.1.0
```

## 🐳 Docker Testing

Tests are also run in the Docker environment as part of the CI/CD pipeline:

```bash
# Build and test in Docker
docker-compose up --build

# Run tests inside container
docker exec -it personal-website-web-1 python -m pytest
```

## 🔄 Continuous Integration

### GitHub Actions Workflow
The `.github/workflows/ci.yml` file includes:

1. **Test Job**: Runs all tests with coverage
2. **Docker Build Job**: Builds and tests Docker container
3. **Security Scan Job**: Runs security linting with Bandit

### Coverage Reporting
- HTML coverage reports generated in `htmlcov/` directory
- Coverage data uploaded to Codecov
- Coverage threshold: 99%

## 🛠️ Troubleshooting

### Common Issues

**Windows File Permission Errors:**
- Tests use temporary databases that are properly cleaned up
- If you see permission errors, the tests will still pass but cleanup may be skipped

**Database Connection Warnings:**
- SQLite connection warnings are normal and don't affect functionality
- Use `--disable-warnings` flag to suppress them

**Import Errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Make sure you're in the project root directory

### Debug Mode
```bash
# Run tests with debug output
python -m pytest -v -s

# Run specific test with debug
python -m pytest test_database.py::TestDatabaseOperations::test_init_db_creates_table -v -s
```

## 📊 Test Results Summary

```
=============================== tests coverage ================================
Name               Stmts   Miss  Cover
--------------------------------------
DAL.py                59      0   100%
app.py                67      2    97%
test_database.py     121      0   100%
test_projects.py     148      0   100%
--------------------------------------
TOTAL                395      2    99%
```

## 🎯 Best Practices

1. **Always run tests before committing code**
2. **Add new tests for new features**
3. **Maintain high test coverage (>95%)**
4. **Use descriptive test names**
5. **Test both success and failure cases**
6. **Keep tests independent and isolated**

## 📝 Adding New Tests

When adding new functionality:

1. **Database changes**: Add tests to `test_database.py`
2. **New routes**: Add tests to `test_projects.py`
3. **New features**: Create new test methods following existing patterns
4. **Edge cases**: Test error conditions and boundary cases

Example test structure:
```python
def test_new_feature(self, client):
    """Test description of what this test verifies."""
    # Arrange
    # Act  
    # Assert
    assert response.status_code == 200
    assert b'expected content' in response.data
```
