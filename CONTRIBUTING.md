# Contributing to NYC Property Investment ML

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/nyc-property-investment-ml.git
   cd nyc-property-investment-ml
   ```
3. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .[dev]  # Install development dependencies
   ```
4. **Run setup and tests**:
   ```bash
   python scripts/setup_project.py
   python scripts/test_system.py
   ```

## 🛠️ Development Workflow

### Creating a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### Making Changes
1. Write your code
2. Add/update tests
3. Update documentation if needed
4. Run tests locally

### Code Quality
We use several tools to maintain code quality:

```bash
# Format code
black src/ scripts/ tests/

# Sort imports
isort src/ scripts/ tests/

# Lint code
flake8 src/ scripts/ tests/

# Run tests
pytest tests/ -v

# Security check
bandit -r src/
```

### Committing Changes
```bash
git add .
git commit -m "feat: add your feature description"
git push origin feature/your-feature-name
```

### Creating a Pull Request
1. Push your branch to your fork
2. Create a pull request from your fork to the main repository
3. Fill out the pull request template
4. Wait for review and CI to pass

## 📝 Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add batch property analysis feature
fix: resolve issue with crime data collection
docs: update API documentation
test: add unit tests for ML model
```

## 🧪 Testing Guidelines

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_model.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run only fast tests (skip slow integration tests)
pytest -m "not slow"
```

### Writing Tests
- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test function names
- Include both unit tests and integration tests
- Mock external API calls in tests

### Test Categories
- `@pytest.mark.unit` - Fast unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.slow` - Slow tests (ML training, etc.)

## 📚 Documentation

### Code Documentation
- Use docstrings for all functions and classes
- Follow Google-style docstrings
- Include type hints where appropriate

### API Documentation
- Update docstrings when changing function signatures
- Include examples in docstrings
- Document expected input/output formats

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Environment details**:
   - Python version
   - Operating system
   - Package versions

2. **Steps to reproduce**:
   - Minimal code example
   - Expected vs actual behavior
   - Error messages and stack traces

3. **Additional context**:
   - Screenshots if applicable
   - Related issues or PRs

## 💡 Feature Requests

When requesting features:

1. **Describe the problem** you're trying to solve
2. **Explain your proposed solution**
3. **Consider alternatives** you've thought about
4. **Provide examples** of how it would be used

## 🎯 Priority Areas for Contribution

We especially welcome contributions in these areas:

### 🔧 Core Features
- **Data Sources**: Integration with more real estate APIs
- **ML Models**: Improved prediction algorithms
- **Location Analysis**: Better neighborhood scoring
- **Risk Assessment**: Enhanced risk modeling

### 🌐 Extensions
- **Web Interface**: Flask/FastAPI web application
- **Mobile App**: React Native mobile application
- **Visualization**: Interactive maps and charts
- **Real-time Data**: Live market data integration

### 📊 Analysis Features
- **Market Trends**: Time series analysis
- **Portfolio Optimization**: Multi-property analysis
- **Comparative Analysis**: Cross-city comparisons
- **Investment Strategies**: Different investment approaches

### 🏙️ Geographic Expansion
- **Other Cities**: Boston, SF, LA, Chicago support
- **International**: London, Toronto, etc.
- **Suburban Markets**: Beyond city centers

## 🔧 Development Setup Details

### Environment Variables
Create a `.env` file:
```bash
GOOGLE_MAPS_API_KEY=your_api_key_here
DATABASE_PATH=data/nyc_property_data.db
LOG_LEVEL=INFO
```

### Database Setup
The SQLite database is created automatically:
```bash
python scripts/setup_project.py
```

### IDE Configuration

#### VS Code
Recommended extensions:
- Python
- Black Formatter
- Pylance
- GitLens

#### PyCharm
Recommended settings:
- Enable Black as external tool
- Configure pytest as test runner
- Set up flake8 as code inspector

## 📋 Code Review Guidelines

### For Contributors
- Keep PRs focused and small
- Write clear commit messages
- Add tests for new features
- Update documentation
- Respond to review feedback promptly

### For Reviewers
- Be constructive and respectful
- Focus on code quality and maintainability
- Check for test coverage
- Verify documentation updates
- Test functionality locally when needed

## 🏗️ Architecture Guidelines

### Code Organization
- `src/`: Main source code
- `scripts/`: Command-line utilities
- `tests/`: Test suite
- `docs/`: Documentation
- `notebooks/`: Jupyter notebooks for analysis

### Design Principles
- **Modularity**: Keep components loosely coupled
- **Testability**: Write testable code with clear interfaces
- **Documentation**: Document public APIs thoroughly
- **Performance**: Optimize for reasonable performance
- **Maintainability**: Write clean, readable code

### External Dependencies
- Minimize external dependencies
- Prefer well-maintained packages
- Pin dependency versions
- Document why each dependency is needed

## 🎉 Recognition

Contributors will be:
- Listed in the README
- Mentioned in release notes
- Given appropriate Git commit credit
- Invited to join the project as maintainers (for significant contributions)

## 📞 Getting Help

- **Issues**: Open a GitHub issue for bugs or questions
- **Discussions**: Use GitHub Discussions for general questions
- **Email**: Contact maintainers for sensitive issues

Thank you for contributing! 🙏
