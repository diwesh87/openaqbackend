"""
OpenAQ API v3 Client
Fetches real-time air quality data from OpenAQ API
"""
import os
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv
import pathlib

# Load .env file from backend directory (for local development)
# In production (Railway), environment variables are provided directly
env_path = pathlib.Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # In production, just load from environment (Railway provides these)
    load_dotenv(override=False)

logger = logging.getLogger(__name__)

OPENAQ_API_BASE = "https://api.openaq.org/v3"
# Strip whitespace and newlines from API key (common issue with environment variables)
API_KEY = os.getenv("OPENAQ_API_KEY", "").strip()

# Fallback to sample data if API fails
USE_FALLBACK = os.getenv("USE_SAMPLE_DATA", "false").lower() == "true"

# Log configuration status (for debugging)
if API_KEY:
    logger.info(f"OpenAQ API Key found: {API_KEY[:10]}... (length: {len(API_KEY)})")
else:
    logger.warning("OpenAQ API Key not found - will use sample data")
    
if USE_FALLBACK:
    logger.warning("USE_SAMPLE_DATA is set to 'true' - will use sample data only")
else:
    logger.info("USE_SAMPLE_DATA is false - will attempt to use OpenAQ API")


def get_headers() -> Dict[str, str]:
    """Get request headers with API key"""
    headers = {
        "Accept": "application/json",
    }
    if API_KEY:
        headers["X-API-Key"] = API_KEY
    return headers


async def fetch_countries() -> List[Dict[str, Any]]:
    """Fetch list of countries from OpenAQ API"""
    if not API_KEY or USE_FALLBACK:
        return []
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{OPENAQ_API_BASE}/countries",
                headers=get_headers(),
                params={"limit": 200}
            )
            response.raise_for_status()
            data = response.json()
            
            countries = []
            for country in data.get("results", []):
                countries.append({
                    "code": country.get("code", ""),
                    "name": country.get("name", ""),
                })
            return countries
    except Exception as e:
        logger.error(f"Error fetching countries from OpenAQ: {e}")
        return []


async def fetch_locations(country_code: str, limit: int = 100) -> List[Dict[str, Any]]:
    """Fetch locations (cities/stations) for a country"""
    if not API_KEY or USE_FALLBACK:
        return []
    
    # Try different parameter formats - OpenAQ API v3 might accept different formats
    param_formats = [
        {"countries": country_code},  # Format 1: 'countries'
        {"countriesId": country_code},  # Format 2: 'countriesId' (camelCase)
        {"countries_id": country_code},  # Format 3: 'countries_id' (snake_case)
    ]
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        for param_format in param_formats:
            try:
                params = {
                    **param_format,
                    "limit": limit,
                    "order_by": "lastUpdated",
                    "sort": "desc"
                }
                
                response = await client.get(
                    f"{OPENAQ_API_BASE}/locations",
                    headers=get_headers(),
                    params=params
                )
                
                # If successful, process the data
                if response.status_code == 200:
                    data = response.json()
                    break
                else:
                    # Log error but try next format
                    error_text = response.text[:500]
                    logger.warning(f"OpenAQ API error for locations (country={country_code}, format={list(param_format.keys())[0]}): Status {response.status_code}, Response: {error_text}")
                    continue
            except Exception as e:
                logger.warning(f"Error trying parameter format {list(param_format.keys())[0]}: {e}")
                continue
        else:
            # All formats failed
            logger.error(f"All parameter formats failed for country {country_code}")
            return []
    
    try:
        locations = []
        for loc in data.get("results", []):
            # Use the location's city field if available, otherwise extract from name
            city_name = loc.get("city") or loc.get("name", "").split(",")[0].strip()
            if not city_name:
                city_name = loc.get("name", "Unknown")
            
            # Get coordinates - OpenAQ API v3 uses 'coordinates' object
            coordinates = loc.get("coordinates", {})
            lat = coordinates.get("latitude") or coordinates.get("lat", 0)
            lon = coordinates.get("longitude") or coordinates.get("lon", 0)
            
            # Get latest measurements from parameters array
            parameters = loc.get("parameters", [])
            measurements = {}
            for param in parameters:
                param_name = param.get("name", "").lower()
                # Try different possible fields for the value
                latest = param.get("lastValue") or param.get("value") or param.get("last_value", 0)
                measurements[param_name] = latest
            
            locations.append({
                "id": loc.get("id", ""),
                "city": city_name,
                "name": loc.get("name", ""),
                "lat": lat,
                "lon": lon,
                "pm25": measurements.get("pm25", 0),
                "pm10": measurements.get("pm10", 0),
                "no2": measurements.get("no2", 0),
                "o3": measurements.get("o3", 0),
                "co": measurements.get("co", 0),
                "so2": measurements.get("so2", 0),
                "lastUpdated": loc.get("lastUpdated") or loc.get("last_updated") or datetime.now().isoformat(),
            })
        
        return locations
    except Exception as e:
        logger.error(f"Error fetching locations for {country_code}: {e}")
        return []


async def fetch_measurements(
    location_id: Optional[str] = None,
    city: Optional[str] = None,
    country_code: Optional[str] = None,
    days: int = 30
) -> List[Dict[str, Any]]:
    """Fetch historical measurements"""
    if not API_KEY or USE_FALLBACK:
        return []
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Calculate date range - OpenAQ API v3 expects ISO 8601 format with timezone
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Format dates as ISO 8601 with 'Z' suffix for UTC
            params = {
                "date_from": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "date_to": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "limit": 1000,
                "order_by": "datetime",
                "sort": "asc"
            }
            
            if location_id:
                params["locations"] = location_id  # Try 'locations' instead of 'locations_id'
            elif city and country_code:
                # We'll need to find location IDs first
                locations = await fetch_locations(country_code, limit=200)
                matching_locs = [loc for loc in locations if city.lower() in loc.get("city", "").lower()]
                if matching_locs:
                    params["locations"] = matching_locs[0].get("id")
                elif country_code:
                    # If no matching city, try filtering by country
                    params["countries"] = country_code
            
            response = await client.get(
                f"{OPENAQ_API_BASE}/measurements",
                headers=get_headers(),
                params=params
            )
            
            # Log error details if request fails
            if response.status_code != 200:
                error_text = response.text[:500]  # First 500 chars of error
                logger.error(f"OpenAQ API error for measurements: Status {response.status_code}, Response: {error_text}")
            
            response.raise_for_status()
            data = response.json()
            
            # Group measurements by date
            measurements_by_date: Dict[str, Dict[str, Any]] = {}
            
            for measurement in data.get("results", []):
                # OpenAQ API v3 might use different date field structures
                date_str = None
                date_obj = measurement.get("date", {})
                if isinstance(date_obj, dict):
                    date_str = date_obj.get("utc") or date_obj.get("local")
                elif isinstance(date_obj, str):
                    date_str = date_obj
                else:
                    # Try datetime field directly
                    date_str = measurement.get("datetime") or measurement.get("dateTime")
                
                if not date_str:
                    continue
                
                # Extract date (YYYY-MM-DD)
                try:
                    # Handle different date formats
                    if isinstance(date_str, str):
                        # Remove timezone info and parse
                        date_str_clean = date_str.replace("Z", "+00:00").split("+")[0].split("T")[0]
                        if len(date_str_clean) == 10:  # YYYY-MM-DD format
                            date_key = date_str_clean
                        else:
                            date_obj_parsed = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                            date_key = date_obj_parsed.strftime("%Y-%m-%d")
                    else:
                        continue
                except Exception as e:
                    logger.debug(f"Error parsing date {date_str}: {e}")
                    continue
                
                if date_key not in measurements_by_date:
                    measurements_by_date[date_key] = {
                        "date": date_key,
                        "pm25": None,
                        "pm10": None,
                        "no2": None,
                        "o3": None,
                        "co": None,
                        "so2": None,
                    }
                
                # Get parameter name - could be nested or direct
                param_obj = measurement.get("parameter", {})
                if isinstance(param_obj, dict):
                    param_name = param_obj.get("name", "").lower()
                else:
                    param_name = str(param_obj).lower()
                
                value = measurement.get("value", 0)
                
                if param_name in measurements_by_date[date_key]:
                    # Use average if multiple values per day
                    current = measurements_by_date[date_key][param_name]
                    if current is None:
                        measurements_by_date[date_key][param_name] = value
                    else:
                        measurements_by_date[date_key][param_name] = (current + value) / 2
            
            # Convert to list and calculate AQI
            history = []
            for date_key in sorted(measurements_by_date.keys()):
                day_data = measurements_by_date[date_key]
                # Calculate AQI from PM2.5 (simplified)
                pm25 = day_data.get("pm25", 0) or 0
                aqi = calculate_aqi_from_pm25(pm25)
                day_data["aqiIndex"] = aqi
                history.append(day_data)
            
            return history
    except Exception as e:
        logger.error(f"Error fetching measurements: {e}")
        return []


def calculate_aqi_from_pm25(pm25: float) -> int:
    """Calculate AQI from PM2.5 value (US EPA standard)"""
    if pm25 <= 12:
        return int((50 / 12) * pm25)
    elif pm25 <= 35.4:
        return int(50 + ((100 - 50) / (35.4 - 12)) * (pm25 - 12))
    elif pm25 <= 55.4:
        return int(100 + ((150 - 100) / (55.4 - 35.4)) * (pm25 - 35.4))
    elif pm25 <= 150.4:
        return int(150 + ((200 - 150) / (150.4 - 55.4)) * (pm25 - 55.4))
    elif pm25 <= 250.4:
        return int(200 + ((300 - 200) / (250.4 - 150.4)) * (pm25 - 150.4))
    else:
        return int(300 + ((400 - 300) / (500.4 - 250.4)) * (pm25 - 250.4))


def get_aqi_category(aqi: int) -> str:
    """Get AQI category from AQI index"""
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


async def aggregate_city_data(locations: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Aggregate location data by city"""
    cities: Dict[str, Dict[str, Any]] = {}
    
    for loc in locations:
        city_name = loc.get("city", "Unknown")
        
        if city_name not in cities:
            cities[city_name] = {
                "city": city_name,
                "pm25": [],
                "pm10": [],
                "no2": [],
                "o3": [],
                "co": [],
                "so2": [],
                "lat": loc.get("lat", 0),
                "lon": loc.get("lon", 0),
                "locations": [],
            }
        
        # Collect measurements from all locations in the city
        if loc.get("pm25", 0) > 0:
            cities[city_name]["pm25"].append(loc["pm25"])
        if loc.get("pm10", 0) > 0:
            cities[city_name]["pm10"].append(loc["pm10"])
        if loc.get("no2", 0) > 0:
            cities[city_name]["no2"].append(loc["no2"])
        if loc.get("o3", 0) > 0:
            cities[city_name]["o3"].append(loc["o3"])
        if loc.get("co", 0) > 0:
            cities[city_name]["co"].append(loc["co"])
        if loc.get("so2", 0) > 0:
            cities[city_name]["so2"].append(loc["so2"])
        
        cities[city_name]["locations"].append(loc)
    
    # Calculate averages for each city
    result = {}
    for city_name, data in cities.items():
        pm25 = sum(data["pm25"]) / len(data["pm25"]) if data["pm25"] else 0
        pm10 = sum(data["pm10"]) / len(data["pm10"]) if data["pm10"] else 0
        no2 = sum(data["no2"]) / len(data["no2"]) if data["no2"] else 0
        o3 = sum(data["o3"]) / len(data["o3"]) if data["o3"] else 0
        co = sum(data["co"]) / len(data["co"]) if data["co"] else 0
        so2 = sum(data["so2"]) / len(data["so2"]) if data["so2"] else 0
        
        aqi = calculate_aqi_from_pm25(pm25)
        
        result[city_name] = {
            "city": city_name,
            "aqiIndex": aqi,
            "aqiCategory": get_aqi_category(aqi),
            "pm25": round(pm25, 1),
            "pm10": round(pm10, 1),
            "no2": round(no2, 1),
            "o3": round(o3, 1),
            "co": round(co, 2),
            "so2": round(so2, 1),
            "lat": data["lat"],
            "lon": data["lon"],
            "population": 0,  # OpenAQ doesn't provide population
            "lastUpdated": datetime.now().isoformat(),
        }
    
    return result

