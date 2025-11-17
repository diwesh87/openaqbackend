# OpenAQ API Integration Setup

## Quick Setup

1. **Create `.env` file in the `backend` directory:**

Create a file named `.env` in the `backend` folder with the following content:

```env
OPENAQ_API_KEY=3fe04e3008c346f2970f4ccea0768554dad106723c784a4824eaf3f8dcf3c6f3
USE_SAMPLE_DATA=false
```

2. **Restart the backend server:**

Stop the current backend server (Ctrl+C) and restart it:
```bash
cd backend
python main.py
```

## Configuration Options

- `OPENAQ_API_KEY`: Your OpenAQ API key (required for real data)
- `USE_SAMPLE_DATA`: Set to `"true"` to use sample data instead of real API calls

## How It Works

The integration automatically:
1. **Tries to fetch real data** from OpenAQ API if API key is provided
2. **Falls back to sample data** if:
   - API key is missing
   - API request fails
   - `USE_SAMPLE_DATA=true` is set

## Testing

After setup, you can test the API:

```bash
# Test countries endpoint
curl http://localhost:8000/api/countries

# Test cities for a country
curl http://localhost:8000/api/cities?country=US

# Test city summary
curl http://localhost:8000/api/city/Los%20Angeles/summary?country=US
```

## Troubleshooting

**If you see "OpenAQ API error, using sample data":**
- Check that your API key is correct in `.env`
- Verify the API key is active at https://docs.openaq.org/
- Check your internet connection
- The system will automatically use sample data as fallback

**To force sample data:**
Set `USE_SAMPLE_DATA=true` in `.env` file

