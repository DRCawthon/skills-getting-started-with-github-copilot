# Mergington High School API Tests

This directory contains unit tests for the Mergington High School API.

## Test Coverage

The tests cover all API endpoints:

- GET `/` - Root redirect
- GET `/activities` - List all activities
- POST `/activities/{activity_name}/signup` - Sign up for an activity
- POST `/activities/{activity_name}/drop` - Drop from an activity

The tests verify both the success cases and error handling for each endpoint. Current test coverage is at 100%.

## Running Tests

To run the tests, make sure you have installed the required packages:

```bash
pip install -r requirements.txt
```

Then run the tests using pytest:

```bash
python -m pytest
```

For more detailed output:

```bash
python -m pytest -v
```

To run tests with coverage reporting:

```bash
python -m pytest --cov=src tests/
```

For a more detailed HTML coverage report:

```bash
python -m pytest --cov=src --cov-report=html tests/
```

This will generate a coverage report in the `htmlcov` directory.

## Test Structure

- `test_app.py` - Contains all the endpoint tests
- `conftest.py` - Contains pytest configuration and shared fixtures
- `__init__.py` - Makes the tests directory a proper Python package

## Adding New Tests

When adding a new test:

1. Follow the existing patterns in `test_app.py`
2. Ensure the test is isolated using the `reset_activities` fixture
3. Name the test function with a `test_` prefix
4. Add appropriate assertions to verify expected behavior