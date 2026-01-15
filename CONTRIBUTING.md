# Contributing to AI-Assisted Insights Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Ways to Contribute

- **Bug Reports**: Found a bug? Open an issue with details on how to reproduce it.
- **Feature Requests**: Have an idea? Open an issue describing the feature and its use case.
- **Code Contributions**: Submit pull requests for bug fixes or new features.
- **Documentation**: Help improve docs, add examples, or fix typos.
- **Testing**: Add test cases or improve test coverage.

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/ai-assisted-insights-agent.git
cd ai-assisted-insights-agent
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install dev dependencies
pip install pytest pytest-asyncio
```

### 3. Run Tests

```bash
pytest tests/ -v
```

## Pull Request Process

### Before Submitting

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write tests** for any new functionality

3. **Run the test suite** to ensure nothing breaks:
   ```bash
   pytest tests/ -v
   ```

4. **Update documentation** if needed

### Submitting Your PR

1. Push your branch to your fork
2. Open a Pull Request against the `main` branch
3. Fill out the PR template with:
   - Description of changes
   - Related issue (if any)
   - Testing performed
4. Wait for review and address any feedback

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic

## Adding New Metrics

To add a new metric definition:

1. Add the metric to `config.yaml`:
   ```yaml
   metrics:
     your_metric:
       name: Your Metric Name
       description: What this metric measures
       sql_template: COUNT(*) or SUM(column)
       table: schema.table_name
       filter: Optional WHERE conditions
       unit: users, dollars, percent, etc.
   ```

2. Add tests in `tests/test_tools.py`

3. Update documentation if the metric is significant

## Adding New MCP Tools

1. Add the tool function in `insights_agent/server.py` with the `@mcp.tool()` decorator
2. Add comprehensive tests in `tests/test_tools.py`
3. Update `docs/API.md` with the new tool's documentation
4. Add usage examples to `examples/USAGE.md`

## Reporting Issues

When reporting issues, please include:

- Python version (`python --version`)
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on the issue, not the person

## Questions?

If you have questions about contributing, feel free to open an issue with the "question" label.

---

Thank you for contributing! 🎉
