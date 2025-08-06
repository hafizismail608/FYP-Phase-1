# Contributing to TransLearn LMS

Thank you for your interest in contributing to TransLearn LMS! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:

- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, browser, etc.)

### Suggesting Features

Feature suggestions are welcome! Please create an issue with:

- A clear, descriptive title
- Detailed description of the proposed feature
- Any relevant examples or mockups
- Explanation of why this feature would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature-name`)
7. Open a Pull Request

#### Pull Request Guidelines

- Follow the existing code style and conventions
- Include tests for new features or bug fixes
- Update documentation as needed
- Keep pull requests focused on a single concern
- Write clear, descriptive commit messages

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and configure environment variables
6. Initialize the database: `python fix_database.py`
7. Run the application: `flask run`

## Testing

Run tests with pytest:

```
pip install pytest pytest-flask
pytest
```

## Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Write docstrings for functions and classes
- Keep functions small and focused on a single task

## License

By contributing to TransLearn LMS, you agree that your contributions will be licensed under the project's MIT License.

## Questions?

If you have any questions about contributing, please contact the development team at support@translearn.com.