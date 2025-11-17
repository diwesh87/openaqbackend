# Backend Setup Guide

Complete setup guide for the OpenAQ Global Air Dashboard Backend.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9 or higher** - [Download](https://www.python.org/downloads/)
- **pip** (Python package manager, comes with Python)
- **Git** - [Download](https://git-scm.com/)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/diwesh87/openaqbackend.git
cd openaqbackend
```

### 2. Create Virtual Environment

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the `backend` directory:

```bash
OPENAQ_API_KEY=your_openaq_api_key_here
USE_SAMPLE_DATA=false
```

Get your OpenAQ API key from: https://openaq.org/

### 5. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 6. Test the API

Open your browser and visit:
- API Root: `http://localhost:8000`
- Interactive Docs: `http://localhost:8000/docs`

## Detailed Setup

### Step-by-Step Installation

#### 1. Verify Python Installation

```bash
python --version
# Should be Python 3.9 or higher

# On some systems, use python3
python3 --version
```

#### 2. Create Virtual Environment

**Why use a virtual environment?**
- Isolates project dependencies
- Prevents conflicts with other Python projects
- Makes deployment easier

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

#### 3. Upgrade pip (Recommended)

```bash
pip install --upgrade pip
```

#### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- FastAPI
- Uvicorn
- httpx
- python-dotenv
- And other dependencies

#### 5. Verify Installation

```bash
pip list
```

You should see all required packages listed.

#### 6. Set Up Environment Variables

Create a `.env` file in the `backend` directory:

```bash
# .env
OPENAQ_API_KEY=your_openaq_api_key_here
USE_SAMPLE_DATA=false
PORT=8000
```

**Getting an OpenAQ API Key:**
1. Visit https://openaq.org/
2. Sign up for an account
3. Navigate to API section
4. Generate an API key
5. Copy the key to your `.env` file

**Important Notes:**
- Never commit `.env` to git (it's in `.gitignore`)
- Keep your API key secure
- The key should not have trailing newlines or spaces

#### 7. Test API Key

```bash
# Start the server
python main.py

# In another terminal, test the key
curl http://localhost:8000/api/test-key
```

#### 8. Run the Server

```bash
python main.py
```

You should see:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Project Structure

```
backend/
├── main.py              # FastAPI application and routes
├── openaq_client.py     # OpenAQ API client
├── data_service.py      # Data service layer with fallbacks
├── sample_data.py       # Sample data for fallback
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore rules
├── Procfile            # Railway deployment config
├── railway.json        # Railway configuration
└── README.md           # Project documentation
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAQ_API_KEY` | OpenAQ API key | None | Yes (for real data) |
| `USE_SAMPLE_DATA` | Use sample data only | `false` | No |
| `PORT` | Server port | `8000` | No (Railway sets this) |

### Using Sample Data

For development/testing without an API key:

```bash
# In .env file
USE_SAMPLE_DATA=true
```

This will use sample data instead of making API calls.

## Running the Server

### Development Mode

```bash
python main.py
```

### Production Mode (with Uvicorn directly)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### With Auto-reload (Development)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing the API

### Using curl

```bash
# Get API info
curl http://localhost:8000/

# Get countries
curl http://localhost:8000/api/countries

# Get cities for India
curl "http://localhost:8000/api/cities?country=IN"

# Get city summary
curl "http://localhost:8000/api/city/New%20Delhi/summary?country=IN"

# Test API key
curl http://localhost:8000/api/test-key
```

### Using Interactive Documentation

FastAPI provides automatic interactive documentation:

1. Start the server: `python main.py`
2. Open browser: `http://localhost:8000/docs`
3. Click "Try it out" on any endpoint
4. Fill in parameters
5. Click "Execute"

### Using Python requests

```python
import requests

# Get countries
response = requests.get("http://localhost:8000/api/countries")
print(response.json())

# Get cities
response = requests.get("http://localhost:8000/api/cities?country=IN")
print(response.json())
```

## Troubleshooting

### Python Not Found

**Error**: `python: command not found`

**Solution**:
- On macOS/Linux, try `python3` instead of `python`
- Ensure Python is installed and in PATH
- Check installation: `python3 --version`

### Virtual Environment Issues

**Error**: `venv: command not found`

**Solution**:
```bash
# Install venv module
python3 -m pip install --user virtualenv

# Then create venv
python3 -m venv venv
```

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Option 1: Use a different port
PORT=8001 python main.py

# Option 2: Kill the process using port 8000
# On macOS/Linux:
lsof -ti:8000 | xargs kill

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### API Key Issues

**Error**: API returns sample data even with API key

**Solution**:
1. Check `.env` file is in `backend/` directory
2. Verify API key has no trailing spaces/newlines
3. Restart the server after changing `.env`
4. Test key: `curl http://localhost:8000/api/test-key`
5. Check server logs for API key status

### Import Errors

**Error**: `ImportError` or `ModuleNotFoundError`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall all dependencies
pip install --upgrade -r requirements.txt

# Verify Python version
python --version  # Should be 3.9+
```

### CORS Errors (Frontend Connection)

**Error**: CORS policy blocking requests

**Solution**:
- The backend is configured to allow all origins
- Check that backend is running
- Verify frontend is using correct API URL
- Check browser console for specific CORS errors

## Development Tips

### Logging

The server logs all requests and errors. Check terminal output for:
- API key status on startup
- Request logs
- Error messages

### Debugging

1. **Check server logs**: All errors are logged to console
2. **Use interactive docs**: Test endpoints at `/docs`
3. **Test with sample data**: Set `USE_SAMPLE_DATA=true` to isolate API issues
4. **Check API key**: Use `/api/test-key` endpoint

### Code Quality

```bash
# Check for syntax errors
python -m py_compile main.py

# Type checking (if using mypy)
pip install mypy
mypy main.py
```

## Production Deployment

### Deploy to Railway

1. **Install Railway CLI** (optional):
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize project**:
   ```bash
   railway init
   ```

4. **Set environment variables** in Railway dashboard:
   - `OPENAQ_API_KEY`: Your API key
   - `USE_SAMPLE_DATA`: `false`

5. **Deploy**:
   ```bash
   railway up
   ```

See `README.md` for more deployment details.

## Next Steps

- Read the [API Documentation](API.md)
- Check the [Contributing Guide](CONTRIBUTING.md)
- Review the [README.md](README.md) for more information
- Explore the codebase starting with `main.py`

## Support

If you encounter issues:
1. Check this guide
2. Review the README.md
3. Check the API.md for endpoint details
4. Open an issue on GitHub
5. Check existing issues for solutions

