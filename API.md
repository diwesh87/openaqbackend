# OpenAQ Global Air Dashboard - API Documentation

Complete API reference for the OpenAQ Global Air Dashboard Backend.

## Base URL

```
http://localhost:8000  # Development
https://your-backend.railway.app  # Production
```

## Authentication

Currently, the API does not require authentication. However, the backend uses an OpenAQ API key internally to fetch data.

## Response Format

All responses are in JSON format. Successful responses return data in the following structure:

```json
{
  "data": [...],
  "message": "Success message (optional)"
}
```

Error responses follow this format:

```json
{
  "detail": "Error message"
}
```

## Endpoints

### 1. Root Endpoint

Get API information and configuration status.

```http
GET /
```

**Response:**
```json
{
  "message": "OpenAQ Global Air Dashboard API",
  "version": "1.0.0",
  "config": {
    "api_key_configured": true,
    "api_key_length": 65,
    "api_key_preview": "3fe04e3008...6f3",
    "use_sample_data": false,
    "data_source": "openaq"
  },
  "endpoints": [
    "/api/countries",
    "/api/cities",
    "/api/city/{city}/summary",
    "/api/city/{city}/history",
    "/api/city/{city}/stations",
    "/api/heatmap",
    "/api/insights",
    "/api/test-key"
  ]
}
```

---

### 2. Get Countries

Retrieve list of all available countries with air quality data.

```http
GET /api/countries
```

**Response:**
```json
{
  "countries": [
    {
      "code": "IN",
      "name": "India"
    },
    {
      "code": "US",
      "name": "United States"
    }
  ]
}
```

**Example:**
```bash
curl http://localhost:8000/api/countries
```

---

### 3. Get Cities

Get list of cities for a specific country.

```http
GET /api/cities?country={country_code}
```

**Parameters:**
- `country` (required, query): Country code (e.g., "IN", "US", "GB")

**Response:**
```json
{
  "country": "IN",
  "cities": [
    {
      "city": "New Delhi",
      "aqiIndex": 156,
      "aqiCategory": "Unhealthy",
      "pm25": 65.2,
      "pm10": 120.5,
      "lat": 28.6139,
      "lon": 77.2090,
      "population": 19000000,
      "lastUpdated": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Example:**
```bash
curl "http://localhost:8000/api/cities?country=IN"
```

**Error Responses:**
- `404 Not Found`: No cities found for the specified country

---

### 4. Get City Summary

Get current air quality summary for a specific city.

```http
GET /api/city/{city}/summary?country={country_code}
```

**Parameters:**
- `city` (required, path): City name (e.g., "New Delhi", "Los Angeles")
- `country` (required, query): Country code

**Response:**
```json
{
  "city": "New Delhi",
  "country": "IN",
  "aqiIndex": 156,
  "aqiCategory": "Unhealthy",
  "pm25": 65.2,
  "pm10": 120.5,
  "no2": 45.3,
  "o3": 32.1,
  "co": 1.2,
  "so2": 18.5,
  "lat": 28.6139,
  "lon": 77.2090,
  "population": 19000000,
  "lastUpdated": "2024-01-15T10:30:00Z"
}
```

**Example:**
```bash
curl "http://localhost:8000/api/city/New%20Delhi/summary?country=IN"
```

**Error Responses:**
- `404 Not Found`: City not found

---

### 5. Get City History

Get historical air quality data for a city.

```http
GET /api/city/{city}/history?country={country_code}&days={days}
```

**Parameters:**
- `city` (required, path): City name
- `country` (required, query): Country code
- `days` (optional, query): Number of days (1-90, default: 30)

**Response:**
```json
{
  "city": "New Delhi",
  "country": "IN",
  "history": [
    {
      "date": "2024-01-15",
      "pm25": 65.2,
      "pm10": 120.5,
      "no2": 45.3,
      "o3": 32.1,
      "co": 1.2,
      "so2": 18.5,
      "aqiIndex": 156
    },
    {
      "date": "2024-01-14",
      "pm25": 62.8,
      "pm10": 118.3,
      "no2": 43.1,
      "o3": 30.5,
      "co": 1.1,
      "so2": 17.2,
      "aqiIndex": 152
    }
  ]
}
```

**Example:**
```bash
curl "http://localhost:8000/api/city/New%20Delhi/history?country=IN&days=7"
```

---

### 6. Get City Stations

Get monitoring stations for a specific city.

```http
GET /api/city/{city}/stations?country={country_code}
```

**Parameters:**
- `city` (required, path): City name
- `country` (required, query): Country code

**Response:**
```json
{
  "city": "New Delhi",
  "country": "IN",
  "stations": [
    {
      "stationName": "Anand Vihar",
      "aqiIndex": 156,
      "pm25": 65.2,
      "pm10": 120.5,
      "latitude": 28.6500,
      "longitude": 77.3167
    },
    {
      "stationName": "RK Puram",
      "aqiIndex": 148,
      "pm25": 58.3,
      "pm10": 112.1,
      "latitude": 28.5667,
      "longitude": 77.1833
    }
  ]
}
```

**Example:**
```bash
curl "http://localhost:8000/api/city/New%20Delhi/stations?country=IN"
```

---

### 7. Get Heatmap Data

Get data points for map visualization.

```http
GET /api/heatmap?country={country_code}
```

**Parameters:**
- `country` (optional, query): Filter by country code

**Response:**
```json
{
  "points": [
    {
      "city": "New Delhi",
      "latitude": 28.6139,
      "longitude": 77.2090,
      "aqiIndex": 156,
      "aqiCategory": "Unhealthy",
      "pm25": 65.2
    },
    {
      "city": "Mumbai",
      "latitude": 19.0760,
      "longitude": 72.8777,
      "aqiIndex": 142,
      "aqiCategory": "Unhealthy for Sensitive Groups",
      "pm25": 58.3
    }
  ]
}
```

**Example:**
```bash
curl "http://localhost:8000/api/heatmap?country=IN"
curl "http://localhost:8000/api/heatmap"  # All countries
```

---

### 8. Get Health Insights

Get health recommendations based on air quality.

```http
GET /api/insights?country={country_code}&city={city}
```

**Parameters:**
- `country` (required, query): Country code
- `city` (required, query): City name

**Response:**
```json
{
  "aqi": 156,
  "category": "Unhealthy",
  "health_advisory": "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.",
  "activity_recommendations": {
    "safe": false,
    "recommendation": "Reduce prolonged or heavy exertion. Avoid outdoor activities.",
    "walking": {
      "safe": false,
      "recommendation": "Avoid outdoor walking. Stay indoors if possible."
    },
    "running": {
      "safe": false,
      "recommendation": "Do not run outdoors. Use indoor alternatives."
    }
  }
}
```

**Example:**
```bash
curl "http://localhost:8000/api/insights?country=IN&city=New%20Delhi"
```

**Error Responses:**
- `404 Not Found`: City not found

---

### 9. Test API Key

Test if the OpenAQ API key is valid and working.

```http
GET /api/test-key
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "API key is valid and working",
  "api_key_length": 65,
  "api_key_preview": "3fe04e3008...6f3",
  "test_response_status": 200
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "API key not configured or too short",
  "api_key_length": 0
}
```

**Example:**
```bash
curl http://localhost:8000/api/test-key
```

---

## HTTP Status Codes

- `200 OK`: Request successful
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Invalid request parameters
- `500 Internal Server Error`: Server error

## Rate Limiting

Currently, there is no rate limiting implemented. However, please be respectful of the API and avoid making excessive requests.

## Error Handling

All errors return a JSON response with a `detail` field:

```json
{
  "detail": "Error message here"
}
```

Common error scenarios:
- Missing required parameters
- Invalid country/city names
- API connection failures (falls back to sample data)
- Invalid date ranges

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces allow you to:
- View all available endpoints
- Test endpoints directly from the browser
- See request/response schemas
- Understand parameter requirements

## Data Sources

The API fetches data from:
- **Primary**: OpenAQ API (https://api.openaq.org/v3)
- **Fallback**: Sample data (when API is unavailable or `USE_SAMPLE_DATA=true`)

## AQI Categories

Air Quality Index (AQI) categories:
- **0-50**: Good
- **51-100**: Moderate
- **101-150**: Unhealthy for Sensitive Groups
- **151-200**: Unhealthy
- **201-300**: Very Unhealthy
- **301+**: Hazardous

## Units

- **PM2.5, PM10**: µg/m³ (micrograms per cubic meter)
- **NO2, O3, SO2**: ppb (parts per billion)
- **CO**: ppm (parts per million)

## Support

For API issues or questions:
- Open an issue on GitHub
- Check the interactive documentation at `/docs`
- Review the backend README.md

