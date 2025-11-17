from datetime import datetime, timedelta
from typing import List, Dict, Any
import random

SAMPLE_COUNTRIES = [
    {"code": "IN", "name": "India"},
    {"code": "US", "name": "United States"},
    {"code": "GB", "name": "United Kingdom"},
    {"code": "DE", "name": "Germany"},
    {"code": "BR", "name": "Brazil"},
    {"code": "CN", "name": "China"},
    {"code": "JP", "name": "Japan"},
    {"code": "AU", "name": "Australia"},
]

SAMPLE_CITIES = {
    "IN": [
        {
            "city": "New Delhi",
            "aqiIndex": 280,
            "aqiCategory": "Very Unhealthy",
            "pm25": 180,
            "pm10": 260,
            "no2": 90,
            "o3": 35,
            "co": 1.2,
            "so2": 22,
            "population": 32000000,
            "lat": 28.7041,
            "lon": 77.1025,
        },
        {
            "city": "Mumbai",
            "aqiIndex": 160,
            "aqiCategory": "Unhealthy",
            "pm25": 95,
            "pm10": 140,
            "no2": 60,
            "o3": 40,
            "co": 0.9,
            "so2": 15,
            "population": 20000000,
            "lat": 19.0760,
            "lon": 72.8777,
        },
        {
            "city": "Bangalore",
            "aqiIndex": 120,
            "aqiCategory": "Unhealthy for Sensitive Groups",
            "pm25": 65,
            "pm10": 95,
            "no2": 45,
            "o3": 38,
            "co": 0.7,
            "so2": 12,
            "population": 12000000,
            "lat": 12.9716,
            "lon": 77.5946,
        },
        {
            "city": "Kolkata",
            "aqiIndex": 185,
            "aqiCategory": "Unhealthy",
            "pm25": 110,
            "pm10": 165,
            "no2": 72,
            "o3": 42,
            "co": 1.0,
            "so2": 18,
            "population": 14800000,
            "lat": 22.5726,
            "lon": 88.3639,
        },
        {
            "city": "Chennai",
            "aqiIndex": 95,
            "aqiCategory": "Moderate",
            "pm25": 48,
            "pm10": 78,
            "no2": 38,
            "o3": 45,
            "co": 0.6,
            "so2": 10,
            "population": 10900000,
            "lat": 13.0827,
            "lon": 80.2707,
        },
    ],
    "US": [
        {
            "city": "Los Angeles",
            "aqiIndex": 75,
            "aqiCategory": "Moderate",
            "pm25": 35,
            "pm10": 58,
            "no2": 42,
            "o3": 55,
            "co": 0.5,
            "so2": 8,
            "population": 13000000,
            "lat": 34.0522,
            "lon": -118.2437,
        },
        {
            "city": "New York",
            "aqiIndex": 55,
            "aqiCategory": "Moderate",
            "pm25": 28,
            "pm10": 45,
            "no2": 38,
            "o3": 48,
            "co": 0.4,
            "so2": 7,
            "population": 19000000,
            "lat": 40.7128,
            "lon": -74.0060,
        },
        {
            "city": "Chicago",
            "aqiIndex": 48,
            "aqiCategory": "Good",
            "pm25": 22,
            "pm10": 38,
            "no2": 32,
            "o3": 42,
            "co": 0.3,
            "so2": 6,
            "population": 9500000,
            "lat": 41.8781,
            "lon": -87.6298,
        },
    ],
    "GB": [
        {
            "city": "London",
            "aqiIndex": 62,
            "aqiCategory": "Moderate",
            "pm25": 32,
            "pm10": 52,
            "no2": 45,
            "o3": 38,
            "co": 0.4,
            "so2": 9,
            "population": 9000000,
            "lat": 51.5074,
            "lon": -0.1278,
        },
        {
            "city": "Manchester",
            "aqiIndex": 58,
            "aqiCategory": "Moderate",
            "pm25": 29,
            "pm10": 48,
            "no2": 40,
            "o3": 35,
            "co": 0.35,
            "so2": 8,
            "population": 2800000,
            "lat": 53.4808,
            "lon": -2.2426,
        },
    ],
    "DE": [
        {
            "city": "Berlin",
            "aqiIndex": 45,
            "aqiCategory": "Good",
            "pm25": 20,
            "pm10": 35,
            "no2": 32,
            "o3": 40,
            "co": 0.3,
            "so2": 6,
            "population": 3800000,
            "lat": 52.5200,
            "lon": 13.4050,
        },
        {
            "city": "Munich",
            "aqiIndex": 42,
            "aqiCategory": "Good",
            "pm25": 18,
            "pm10": 32,
            "no2": 28,
            "o3": 38,
            "co": 0.28,
            "so2": 5,
            "population": 1500000,
            "lat": 48.1351,
            "lon": 11.5820,
        },
    ],
    "BR": [
        {
            "city": "São Paulo",
            "aqiIndex": 88,
            "aqiCategory": "Moderate",
            "pm25": 42,
            "pm10": 68,
            "no2": 52,
            "o3": 45,
            "co": 0.65,
            "so2": 12,
            "population": 22000000,
            "lat": -23.5505,
            "lon": -46.6333,
        },
        {
            "city": "Rio de Janeiro",
            "aqiIndex": 72,
            "aqiCategory": "Moderate",
            "pm25": 36,
            "pm10": 58,
            "no2": 45,
            "o3": 50,
            "co": 0.55,
            "so2": 10,
            "population": 13000000,
            "lat": -22.9068,
            "lon": -43.1729,
        },
    ],
    "CN": [
        {
            "city": "Beijing",
            "aqiIndex": 165,
            "aqiCategory": "Unhealthy",
            "pm25": 98,
            "pm10": 145,
            "no2": 68,
            "o3": 42,
            "co": 0.95,
            "so2": 20,
            "population": 21500000,
            "lat": 39.9042,
            "lon": 116.4074,
        },
        {
            "city": "Shanghai",
            "aqiIndex": 135,
            "aqiCategory": "Unhealthy for Sensitive Groups",
            "pm25": 78,
            "pm10": 115,
            "no2": 58,
            "o3": 48,
            "co": 0.82,
            "so2": 16,
            "population": 27000000,
            "lat": 31.2304,
            "lon": 121.4737,
        },
    ],
    "JP": [
        {
            "city": "Tokyo",
            "aqiIndex": 52,
            "aqiCategory": "Moderate",
            "pm25": 26,
            "pm10": 42,
            "no2": 36,
            "o3": 45,
            "co": 0.38,
            "so2": 7,
            "population": 37000000,
            "lat": 35.6762,
            "lon": 139.6503,
        },
        {
            "city": "Osaka",
            "aqiIndex": 48,
            "aqiCategory": "Good",
            "pm25": 23,
            "pm10": 38,
            "no2": 32,
            "o3": 42,
            "co": 0.35,
            "so2": 6,
            "population": 19000000,
            "lat": 34.6937,
            "lon": 135.5023,
        },
    ],
    "AU": [
        {
            "city": "Sydney",
            "aqiIndex": 38,
            "aqiCategory": "Good",
            "pm25": 15,
            "pm10": 28,
            "no2": 25,
            "o3": 38,
            "co": 0.25,
            "so2": 4,
            "population": 5300000,
            "lat": -33.8688,
            "lon": 151.2093,
        },
        {
            "city": "Melbourne",
            "aqiIndex": 35,
            "aqiCategory": "Good",
            "pm25": 14,
            "pm10": 25,
            "no2": 22,
            "o3": 35,
            "co": 0.22,
            "so2": 3,
            "population": 5000000,
            "lat": -37.8136,
            "lon": 144.9631,
        },
    ],
}


def generate_historical_data(city: str, days: int = 30) -> List[Dict[str, Any]]:
    base_data = None
    for country_cities in SAMPLE_CITIES.values():
        for city_data in country_cities:
            if city_data["city"] == city:
                base_data = city_data
                break
        if base_data:
            break

    if not base_data:
        base_data = {"pm25": 50, "pm10": 75, "aqiIndex": 100}

    history = []
    base_date = datetime.now()

    for i in range(days, 0, -1):
        date = base_date - timedelta(days=i)
        variation = random.uniform(0.7, 1.3)
        seasonal_factor = 1 + 0.2 * (i % 7 - 3) / 7

        history.append({
            "date": date.strftime("%Y-%m-%d"),
            "pm25": round(base_data["pm25"] * variation * seasonal_factor, 1),
            "pm10": round(base_data["pm10"] * variation * seasonal_factor, 1),
            "no2": round(base_data.get("no2", 40) * variation, 1),
            "o3": round(base_data.get("o3", 40) * variation, 1),
            "co": round(base_data.get("co", 0.5) * variation, 2),
            "so2": round(base_data.get("so2", 10) * variation, 1),
            "aqiIndex": round(base_data["aqiIndex"] * variation * seasonal_factor),
        })

    return history


def generate_stations(city: str, country_code: str) -> List[Dict[str, Any]]:
    city_data = None
    for city_entry in SAMPLE_CITIES.get(country_code, []):
        if city_entry["city"] == city:
            city_data = city_entry
            break

    if not city_data:
        return []

    stations = []
    station_names = [
        f"{city} Central",
        f"{city} North",
        f"{city} South",
        f"{city} East",
        f"{city} West",
    ]

    for i, name in enumerate(station_names[:3]):
        lat_offset = random.uniform(-0.05, 0.05)
        lon_offset = random.uniform(-0.05, 0.05)
        variation = random.uniform(0.8, 1.2)

        stations.append({
            "stationName": name,
            "latitude": round(city_data["lat"] + lat_offset, 4),
            "longitude": round(city_data["lon"] + lon_offset, 4),
            "pm25": round(city_data["pm25"] * variation, 1),
            "pm10": round(city_data["pm10"] * variation, 1),
            "no2": round(city_data["no2"] * variation, 1),
            "o3": round(city_data["o3"] * variation, 1),
            "co": round(city_data["co"] * variation, 2),
            "so2": round(city_data["so2"] * variation, 1),
            "aqiIndex": round(city_data["aqiIndex"] * variation),
            "lastUpdated": datetime.now().isoformat(),
        })

    return stations


def get_aqi_category(aqi: int) -> str:
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


def get_countries() -> List[Dict[str, Any]]:
    result = []
    for country in SAMPLE_COUNTRIES:
        cities = SAMPLE_CITIES.get(country["code"], [])
        if cities:
            avg_aqi = sum(c["aqiIndex"] for c in cities) / len(cities)
            worst_city = max(cities, key=lambda c: c["aqiIndex"])

            result.append({
                "code": country["code"],
                "name": country["name"],
                "cityCount": len(cities),
                "averageAqi": round(avg_aqi),
                "worstCity": worst_city["city"],
                "worstCityAqi": worst_city["aqiIndex"],
            })

    return result


def get_cities(country_code: str) -> List[Dict[str, Any]]:
    cities = SAMPLE_CITIES.get(country_code, [])
    now = datetime.now().isoformat()

    return [
        {
            **city,
            "lastUpdated": now,
        }
        for city in cities
    ]


def get_city_summary(city: str, country_code: str) -> Dict[str, Any]:
    cities = SAMPLE_CITIES.get(country_code, [])
    for city_data in cities:
        if city_data["city"] == city:
            return {
                **city_data,
                "lastUpdated": datetime.now().isoformat(),
            }
    return None
