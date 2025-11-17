# OpenAQ Global Air Dashboard - Backend API

A FastAPI-based backend service that provides air quality data from the OpenAQ API. This service acts as a middleware layer, handling API authentication, data transformation, and fallback mechanisms.

## 🌟 Features

- **OpenAQ API Integration**: Fetches real-time air quality data
- **Fallback System**: Gracefully falls back to sample data if API fails
- **Data Transformation**: Converts OpenAQ data to dashboard-friendly format
- **CORS Enabled**: Ready for frontend integration
- **Async/Await**: High-performance async operations
- **Error Handling**: Robust error handling with fallbacks

## 🚀 Tech Stack

- **FastAPI** - Modern Python web framework
- **Python 3.9+** - Programming language
- **httpx** - Async HTTP client
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd openaq-dashboard/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   OPENAQ_API_KEY=your_openaq_api_key_here
   USE_SAMPLE_DATA=false
   ```

   Get your OpenAQ API key from: https://openaq.org/

5. **Run the server**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Get Countries
```http
GET /api/countries
```
Returns list of all available countries with air quality data.

#### Get Cities
```http
GET /api/cities?country={country_code}
```
Returns list of cities for a specific country.

**Parameters:**
- `country` (required): Country code (e.g., "IN", "US")

#### Get City Summary
```http
GET /api/city/{city}/summary?country={country_code}
```
Returns current air quality summary for a city.

**Parameters:**
- `city` (path): City name (e.g., "New Delhi")
- `country` (query, required): Country code

#### Get City History
```http
GET /api/city/{city}/history?country={country_code}&days={days}
```
Returns historical air quality data for a city.

**Parameters:**
- `city` (path): City name
- `country` (query, required): Country code
- `days` (query, optional): Number of days (1-90, default: 30)

#### Get City Stations
```http
GET /api/city/{city}/stations?country={country_code}
```
Returns monitoring stations for a city.

#### Get Heatmap Data
```http
GET /api/heatmap?country={country_code}
```
Returns data points for map visualization.

**Parameters:**
- `country` (query, optional): Filter by country code

#### Get Health Insights
```http
GET /api/insights?country={country_code}&city={city}
```
Returns health recommendations based on air quality.

### API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🌐 Deployment

This backend is designed to be deployed on **Railways**.

### Deploy to Railways

1. **Install Railways CLI** (optional)
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railways**
   ```bash
   railway login
   ```

3. **Initialize project**
   ```bash
   railway init
   ```

4. **Set environment variables**
   ```bash
   railway variables set OPENAQ_API_KEY=your_api_key_here
   railway variables set USE_SAMPLE_DATA=false
   ```

5. **Deploy**
   ```bash
   railway up
   ```

### Environment Variables

- `OPENAQ_API_KEY` - Your OpenAQ API key (required for real data)
- `USE_SAMPLE_DATA` - Set to "true" to use sample data only (default: "false")
- `PORT` - Server port (Railways sets this automatically)

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI application and routes
├── openaq_client.py     # OpenAQ API client
├── data_service.py      # Data service layer with fallbacks
├── sample_data.py       # Sample data for fallback
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
└── README.md           # This file
```

## 🔧 Configuration

### OpenAQ API Setup

1. Sign up at https://openaq.org/
2. Get your API key from the dashboard
3. Add it to your `.env` file:
   ```
   OPENAQ_API_KEY=your_key_here
   ```

### Fallback Mode

If you want to use sample data only (for development/testing):

```bash
USE_SAMPLE_DATA=true
```

## 🧪 Testing

Test the API endpoints using curl or the interactive docs:

```bash
# Get countries
curl http://localhost:8000/api/countries

# Get cities for India
curl http://localhost:8000/api/cities?country=IN

# Get city summary
curl http://localhost:8000/api/city/New%20Delhi/summary?country=IN
```

## 🔒 CORS Configuration

The API is configured to allow requests from:
- `http://localhost:5173` (Vite dev server)
- Your Vercel deployment URL (update in `main.py` if needed)

## 📊 Data Flow

1. **Request** → FastAPI endpoint
2. **Data Service** → Checks if OpenAQ API should be used
3. **OpenAQ Client** → Fetches data from OpenAQ API
4. **Fallback** → Uses sample data if API fails
5. **Transform** → Converts to dashboard format
6. **Response** → Returns JSON to frontend

## 🤝 Contributing

This is an open-source project! Contributions are welcome. Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [OpenAQ](https://openaq.org/) for providing air quality data
- [FastAPI](https://fastapi.tiangolo.com/) for the amazing framework
- All contributors who help improve this API

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.

## 🐛 Troubleshooting

### API Key Issues
- Ensure your `.env` file is in the `backend/` directory
- Check that the API key is correctly formatted
- Verify the key is valid at https://openaq.org/

### Port Already in Use
- Change the port in `main.py` or set `PORT` environment variable
- Kill the process using the port: `lsof -ti:8000 | xargs kill` (macOS/Linux)

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version: `python --version` (should be 3.9+)

