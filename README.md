# Data Pipeline QA Test Suite

Automated regression and validation tests for data processing pipelines.

## Features

- **Data Quality Validation**: Comprehensive checks for data completeness, accuracy, and consistency
- **Business Rules Validation**: Configurable business logic validation  
- **Performance Testing**: Throughput, latency, and memory usage benchmarks
- **Regression Testing**: Detect changes in pipeline behavior over time
- **CI/CD Integration**: Automated testing in GitHub Actions

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run all tests:**
   ```bash
   pytest
   ```

3. **Run specific test categories:**
   ```bash
   pytest -m unit          # Unit tests only
   pytest -m integration   # Integration tests only
   pytest -m regression    # Regression tests only
   ```

4. **Generate test report:**
   ```bash
   pytest --html=reports/test_report.html
   ```

## Project Structure

```
data-pipeline-qa/
├── src/                 # Source code
├── tests/              # Test suites
├── configs/            # Configuration files
├── data/               # Test datasets and baselines
├── scripts/            # Utility scripts
└── reports/            # Generated test reports
```