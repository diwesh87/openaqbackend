"""
Data Service - Fetches data from OpenAQ API with fallback to sample data
"""
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

from openaq_client import (
    fetch_countries as fetch_openaq_countries,
    fetch_locations,
    fetch_measurements,
    aggregate_city_data,
    calculate_aqi_from_pm25,
    API_KEY,
    USE_FALLBACK,
)
from sample_data import (
    get_countries as get_sample_countries,
    get_cities as get_sample_cities,
    get_city_summary as get_sample_city_summary,
    generate_historical_data as generate_sample_historical_data,
    generate_stations as generate_sample_stations,
    SAMPLE_CITIES,
    get_aqi_category,
)


def use_openaq() -> bool:
    """Check if we should use OpenAQ API"""
    return bool(API_KEY) and not USE_FALLBACK


async def get_countries() -> List[Dict[str, Any]]:
    """Get countries - try OpenAQ first, fallback to sample"""
    if use_openaq():
        try:
            openaq_countries = await fetch_openaq_countries()
            if openaq_countries:
                # Transform to our format
                result = []
                for country in openaq_countries:
                    result.append({
                        "code": country.get("code", ""),
                        "name": country.get("name", ""),
                        "cityCount": 0,  # Will be calculated
                        "averageAqi": 0,
                        "worstCity": "",
                        "worstCityAqi": 0,
                    })
                
                # Add USA if not present (OpenAQ might not have it)
                us_found = any(c.get("code") == "US" for c in result)
                if not us_found:
                    # Get sample USA data and add it
                    sample_countries = get_sample_countries()
                    us_sample = next((c for c in sample_countries if c.get("code") == "US"), None)
                    if us_sample:
                        result.append(us_sample)
                
                return result
        except Exception as e:
            print(f"OpenAQ API error, using sample data: {e}")
    
    # Fallback to sample data
    return get_sample_countries()


async def get_cities(country_code: str) -> List[Dict[str, Any]]:
    """Get cities for a country - try OpenAQ first, fallback to sample"""
    if use_openaq():
        try:
            locations = await fetch_locations(country_code, limit=200)
            if locations:
                # Aggregate by city
                city_data = await aggregate_city_data(locations)
                cities_list = list(city_data.values())
                if cities_list:
                    return cities_list
        except Exception as e:
            print(f"OpenAQ API error, using sample data: {e}")
    
    # Fallback to sample data
    return get_sample_cities(country_code)


async def get_city_summary(city: str, country_code: str) -> Optional[Dict[str, Any]]:
    """Get city summary - try OpenAQ first, fallback to sample"""
    if use_openaq():
        try:
            locations = await fetch_locations(country_code, limit=200)
            if locations:
                city_data = await aggregate_city_data(locations)
                # Try exact match first, then case-insensitive
                if city in city_data:
                    return city_data[city]
                # Try case-insensitive match
                for city_name, data in city_data.items():
                    if city.lower() == city_name.lower():
                        return data
        except Exception as e:
            print(f"OpenAQ API error, using sample data: {e}")
    
    # Fallback to sample data
    return get_sample_city_summary(city, country_code)


async def get_city_history(city: str, country_code: str, days: int = 30) -> List[Dict[str, Any]]:
    """Get city historical data - try OpenAQ first, fallback to sample"""
    if use_openaq():
        try:
            history = await fetch_measurements(city=city, country_code=country_code, days=days)
            if history:
                return history
        except Exception as e:
            print(f"OpenAQ API error, using sample data: {e}")
    
    # Fallback to sample data
    return generate_sample_historical_data(city, days)


async def get_city_stations(city: str, country_code: str) -> List[Dict[str, Any]]:
    """Get city stations - try OpenAQ first, fallback to sample"""
    if use_openaq():
        try:
            locations = await fetch_locations(country_code, limit=200)
            if locations:
                # Filter locations for this city
                city_locations = [
                    loc for loc in locations
                    if city.lower() in loc.get("city", "").lower()
                ]
                
                stations = []
                for loc in city_locations[:5]:  # Limit to 5 stations
                    pm25 = loc.get("pm25", 0)
                    aqi = calculate_aqi_from_pm25(pm25) if pm25 > 0 else 0
                    
                    stations.append({
                        "stationName": loc.get("name", "Unknown Station"),
                        "latitude": loc.get("lat", 0),
                        "longitude": loc.get("lon", 0),
                        "pm25": round(loc.get("pm25", 0), 1),
                        "pm10": round(loc.get("pm10", 0), 1),
                        "no2": round(loc.get("no2", 0), 1),
                        "o3": round(loc.get("o3", 0), 1),
                        "co": round(loc.get("co", 0), 2),
                        "so2": round(loc.get("so2", 0), 1),
                        "aqiIndex": aqi,
                        "lastUpdated": loc.get("lastUpdated", datetime.now().isoformat()),
                    })
                
                if stations:
                    return stations
        except Exception as e:
            print(f"OpenAQ API error, using sample data: {e}")
    
    # Fallback to sample data
    return generate_sample_stations(city, country_code)


async def get_heatmap_points(country_code: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get heatmap points - try OpenAQ first, fallback to sample data"""
    if use_openaq() and country_code:
        try:
            locations = await fetch_locations(country_code, limit=200)
            if locations:
                city_data = await aggregate_city_data(locations)
                points = []
                for city_name, data in city_data.items():
                    points.append({
                        "city": city_name,
                        "country": country_code,
                        "latitude": data.get("lat", 0),
                        "longitude": data.get("lon", 0),
                        "pm25": data.get("pm25", 0),
                        "aqiIndex": data.get("aqiIndex", 0),
                        "aqiCategory": data.get("aqiCategory", "Unknown"),
                    })
                if points:
                    return points
        except Exception as e:
            print(f"OpenAQ API error for heatmap, using sample data: {e}")
    
    # Fallback to sample data
    points = []
    if country_code:
        cities = SAMPLE_CITIES.get(country_code, [])
        for city_data in cities:
            points.append({
                "city": city_data["city"],
                "country": country_code,
                "latitude": city_data["lat"],
                "longitude": city_data["lon"],
                "pm25": city_data["pm25"],
                "aqiIndex": city_data["aqiIndex"],
                "aqiCategory": city_data["aqiCategory"],
            })
    else:
        for country_code, cities in SAMPLE_CITIES.items():
            for city_data in cities:
                points.append({
                    "city": city_data["city"],
                    "country": country_code,
                    "latitude": city_data["lat"],
                    "longitude": city_data["lon"],
                    "pm25": city_data["pm25"],
                    "aqiIndex": city_data["aqiIndex"],
                    "aqiCategory": city_data["aqiCategory"],
                })
    
    return points

