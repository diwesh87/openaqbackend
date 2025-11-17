# Contributing to OpenAQ Global Air Dashboard - Backend

Thank you for your interest in contributing to the OpenAQ Global Air Dashboard Backend! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- **Clear title and description**
- **Steps to reproduce** the bug
- **Expected vs actual behavior**
- **Error messages** (if any)
- **Python version** and environment details

### Suggesting Features

We welcome feature suggestions! Please open an issue with:
- **Clear description** of the feature
- **Use case** - why would this be useful?
- **Possible implementation** (if you have ideas)

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/openaqbackend.git
   cd openaqbackend
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   OPENAQ_API_KEY=your_api_key_here
   USE_SAMPLE_DATA=false
   ```

5. **Make your changes**
   - Follow PEP 8 style guidelines
   - Write clear, readable code
   - Add docstrings for functions/classes
   - Handle errors gracefully
   - Update documentation if needed

6. **Test your changes**
   ```bash
   python main.py
   # Test endpoints using curl or the interactive docs at http://localhost:8000/docs
   ```

7. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   # or
   git commit -m "fix: fix your bug description"
   ```

   **Commit message format:**
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `style:` for formatting changes
   - `refactor:` for code refactoring
   - `test:` for adding tests
   - `chore:` for maintenance tasks

8. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

9. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template
   - Wait for review

## 📋 Code Style Guidelines

### Python Style
- Follow **PEP 8** style guide
- Use **type hints** for function parameters and return types
- Maximum line length: **88 characters** (Black formatter default)
- Use **f-strings** for string formatting
- Use **snake_case** for variables and functions
- Use **PascalCase** for classes

### FastAPI Best Practices
- Use **async/await** for I/O operations
- Define proper **Pydantic models** for request/response
- Use **dependency injection** where appropriate
- Add proper **HTTP status codes**
- Include **error handling** with try/except

### Error Handling
- Always handle exceptions gracefully
- Return appropriate HTTP status codes
- Provide meaningful error messages
- Log errors for debugging

### Documentation
- Add **docstrings** to all functions and classes
- Use Google-style docstrings:
  ```python
  def fetch_data(country: str) -> List[Dict]:
      """Fetch air quality data for a country.
      
      Args:
          country: Country code (e.g., 'IN', 'US')
      
      Returns:
          List of dictionaries containing air quality data
      
      Raises:
          HTTPException: If API call fails
      """
  ```

## 🧪 Testing

Before submitting a PR, ensure:
- [ ] Code runs without errors
- [ ] All endpoints work correctly
- [ ] Error handling is tested
- [ ] API documentation is updated
- [ ] No new warnings generated
- [ ] Environment variables are properly handled

### Testing Endpoints

```bash
# Get countries
curl http://localhost:8000/api/countries

# Get cities
curl http://localhost:8000/api/cities?country=IN

# Get city summary
curl http://localhost:8000/api/city/New%20Delhi/summary?country=IN

# Use interactive docs
# Visit http://localhost:8000/docs
```

## 📝 Pull Request Checklist

- [ ] Code follows PEP 8 style guidelines
- [ ] Self-review completed
- [ ] Docstrings added for new functions/classes
- [ ] Error handling implemented
- [ ] Documentation updated (if needed)
- [ ] No new warnings generated
- [ ] Changes tested locally
- [ ] PR description is clear and detailed

## 🏗️ Project Structure

```
backend/
├── main.py              # FastAPI app and routes
├── openaq_client.py     # OpenAQ API client
├── data_service.py      # Data service layer
├── sample_data.py       # Sample data fallback
├── requirements.txt     # Dependencies
└── .env                 # Environment variables (not in git)
```

## 🔧 Development Tips

### Running the Server
```bash
python main.py
# Server runs on http://localhost:8000
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Environment Variables
- Always use `.env` file for local development
- Never commit `.env` to git
- Document new environment variables in README

### Debugging
- Use FastAPI's automatic documentation
- Check server logs for errors
- Use Python's logging module
- Test with sample data first (`USE_SAMPLE_DATA=true`)

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python PEP 8](https://pep8.org/)
- [OpenAQ API Docs](https://docs.openaq.org/)
- [httpx Documentation](https://www.python-httpx.org/)

## ❓ Questions?

If you have questions:
- Open an issue with the `question` label
- Check existing issues and discussions
- Review the README.md for setup instructions

## 🙏 Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!

