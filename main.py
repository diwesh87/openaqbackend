from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from dotenv import load_dotenv

from data_service import (
    get_countries,
    get_cities,
    get_city_summary,
    get_city_history,
    get_city_stations,
    get_heatmap_points,
)
import httpx
from sample_data import SAMPLE_CITIES
import pathlib

# Load .env file from backend directory (for local development)
# In production (Railway), environment variables are provided directly
env_path = pathlib.Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # In production, just load from environment (Railway provides these)
    load_dotenv(override=False)

# Log environment status
import logging
logger = logging.getLogger(__name__)
api_key = os.getenv("OPENAQ_API_KEY", "")
use_sample = os.getenv("USE_SAMPLE_DATA", "false").lower() == "true"
logger.info(f"Environment check - API_KEY present: {bool(api_key)}, USE_SAMPLE_DATA: {use_sample}")

app = FastAPI(title="OpenAQ Global Air Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    api_key = os.getenv("OPENAQ_API_KEY", "")
    # Check if API key exists and is not empty (has reasonable length)
    api_key_set = bool(api_key) and len(api_key.strip()) > 10
    use_sample = os.getenv("USE_SAMPLE_DATA", "false").lower() == "true"
    
    # Show masked API key for debugging (first 10 chars + last 4 chars)
    api_key_preview = ""
    if api_key:
        if len(api_key) > 14:
            api_key_preview = f"{api_key[:10]}...{api_key[-4:]}"
        else:
            api_key_preview = f"{api_key[:6]}...{api_key[-2:]}" if len(api_key) > 8 else "***"
    
    return {
        "message": "OpenAQ Global Air Dashboard API",
        "version": "1.0.0",
        "config": {
            "api_key_configured": api_key_set,
            "api_key_length": len(api_key) if api_key else 0,
            "api_key_preview": api_key_preview,
            "use_sample_data": use_sample,
            "data_source": "sample" if (not api_key_set or use_sample) else "openaq",
        },
        "endpoints": [
            "/api/countries",
            "/api/cities",
            "/api/city/{city}/summary",
            "/api/city/{city}/history",
            "/api/city/{city}/stations",
            "/api/heatmap",
            "/api/insights",
            "/api/test-key",  # New endpoint to test API key
        ],
    }


@app.get("/api/test-key")
async def test_api_key():
    """Test if the OpenAQ API key is working"""
    api_key = os.getenv("OPENAQ_API_KEY", "")
    
    if not api_key or len(api_key.strip()) < 10:
        return {
            "status": "error",
            "message": "API key not configured or too short",
            "api_key_length": len(api_key) if api_key else 0,
        }
    
    try:
        # Try to make a simple API call to test the key
        async with httpx.AsyncClient(timeout=10.0) as client:
            headers = {
                "Accept": "application/json",
                "X-API-Key": api_key,
            }
            # Try fetching countries as a simple test
            response = await client.get(
                "https://api.openaq.org/v3/countries",
                headers=headers,
                params={"limit": 1}
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "API key is valid and working",
                    "api_key_length": len(api_key),
                    "api_key_preview": f"{api_key[:10]}...{api_key[-4:]}",
                    "test_response_status": response.status_code,
                }
            elif response.status_code == 401:
                return {
                    "status": "error",
                    "message": "API key is invalid or unauthorized",
                    "api_key_length": len(api_key),
                    "api_key_preview": f"{api_key[:10]}...{api_key[-4:]}",
                    "test_response_status": response.status_code,
                    "error": "Unauthorized - check your API key",
                }
            else:
                error_text = response.text[:200]
                return {
                    "status": "error",
                    "message": f"API call failed with status {response.status_code}",
                    "api_key_length": len(api_key),
                    "api_key_preview": f"{api_key[:10]}...{api_key[-4:]}",
                    "test_response_status": response.status_code,
                    "error": error_text,
                }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error testing API key: {str(e)}",
            "api_key_length": len(api_key) if api_key else 0,
        }


@app.get("/api/countries")
async def list_countries():
    countries = await get_countries()
    return {"countries": countries}


@app.get("/api/cities")
async def list_cities(country: str = Query(..., description="Country code (e.g., IN, US)")):
    cities = await get_cities(country)
    if not cities:
        raise HTTPException(status_code=404, detail=f"No cities found for country: {country}")
    return {"country": country, "cities": cities}


@app.get("/api/city/{city}/summary")
async def city_summary(
    city: str,
    country: str = Query(..., description="Country code (e.g., IN, US)"),
):
    summary = await get_city_summary(city, country)
    if not summary:
        raise HTTPException(status_code=404, detail=f"City not found: {city}")
    return summary


@app.get("/api/city/{city}/history")
async def city_history(
    city: str,
    country: str = Query(..., description="Country code (e.g., IN, US)"),
    days: int = Query(30, description="Number of days of history", ge=1, le=90),
):
    history = await get_city_history(city, country, days)
    return {"city": city, "country": country, "history": history}


@app.get("/api/city/{city}/stations")
async def city_stations(
    city: str,
    country: str = Query(..., description="Country code (e.g., IN, US)"),
):
    stations = await get_city_stations(city, country)
    return {"city": city, "country": country, "stations": stations}


@app.get("/api/heatmap")
async def heatmap(country: Optional[str] = Query(None, description="Country code filter")):
    points = await get_heatmap_points(country)
    return {"points": points}


@app.get("/api/insights")
async def get_insights(
    country: str = Query(..., description="Country code"),
    city: str = Query(..., description="City name"),
):
    summary = await get_city_summary(city, country)
    if not summary:
        raise HTTPException(status_code=404, detail=f"City not found: {city}")

    aqi = summary["aqiIndex"]
    category = summary["aqiCategory"]

    insights = {
        "city": city,
        "country": country,
        "aqi": aqi,
        "category": category,
        "health": {},
        "activities": {},
    }

    if aqi <= 50:
        insights["health"] = {
            "general": "Air quality is excellent. No health concerns.",
            "sensitive": "Perfect conditions for everyone, including sensitive groups.",
            "children": "Ideal for outdoor play and activities.",
            "elderly": "Safe for all outdoor activities.",
            "asthma": "No restrictions for asthma patients.",
        }
        insights["activities"] = {
            "walking": {"safe": True, "recommendation": "Excellent for walking at any pace."},
            "running": {"safe": True, "recommendation": "Perfect for long runs and intense workouts."},
            "outdoor_play": {"safe": True, "recommendation": "Great day for kids to play outside."},
            "cycling": {"safe": True, "recommendation": "Ideal conditions for cycling."},
        }
    elif aqi <= 100:
        insights["health"] = {
            "general": "Air quality is acceptable. Most people can engage in outdoor activities.",
            "sensitive": "Unusually sensitive people may experience minor symptoms.",
            "children": "Generally safe, but watch for any unusual symptoms.",
            "elderly": "Safe for moderate outdoor activities.",
            "asthma": "Most asthma patients can go about normal activities. Monitor for symptoms.",
        }
        insights["activities"] = {
            "walking": {"safe": True, "recommendation": "Good for walking. No restrictions."},
            "running": {"safe": True, "recommendation": "Safe for running, but sensitive individuals should monitor how they feel."},
            "outdoor_play": {"safe": True, "recommendation": "Children can play outside normally."},
            "cycling": {"safe": True, "recommendation": "Good conditions for cycling."},
        }
    elif aqi <= 150:
        insights["health"] = {
            "general": "Sensitive groups may experience health effects.",
            "sensitive": "People with heart or lung disease, children, and older adults should reduce prolonged outdoor exertion.",
            "children": "Active children should take breaks and reduce intense outdoor activities.",
            "elderly": "Older adults should limit prolonged outdoor exertion.",
            "asthma": "Asthma patients may experience symptoms. Keep quick-relief inhaler handy.",
        }
        insights["activities"] = {
            "walking": {"safe": True, "recommendation": "Light to moderate walking is okay. Sensitive groups should limit duration."},
            "running": {"safe": False, "recommendation": "Avoid intense running. Sensitive groups should skip outdoor workouts."},
            "outdoor_play": {"safe": True, "recommendation": "Limit prolonged or intense outdoor play for children."},
            "cycling": {"safe": True, "recommendation": "Moderate cycling is okay, but avoid intense efforts."},
        }
    elif aqi <= 200:
        insights["health"] = {
            "general": "Everyone may begin to experience health effects. Sensitive groups may experience more serious effects.",
            "sensitive": "People with heart or lung disease, children, and older adults should avoid prolonged outdoor exertion.",
            "children": "Children should limit outdoor play and avoid strenuous activities.",
            "elderly": "Elderly should stay indoors and avoid exertion.",
            "asthma": "Asthma patients should avoid outdoor activities. Use medications as prescribed.",
        }
        insights["activities"] = {
            "walking": {"safe": True, "recommendation": "Short walks are acceptable, but limit time outdoors."},
            "running": {"safe": False, "recommendation": "Avoid running and intense outdoor workouts entirely."},
            "outdoor_play": {"safe": False, "recommendation": "Children should play indoors. Avoid outdoor activities."},
            "cycling": {"safe": False, "recommendation": "Avoid cycling. Use indoor alternatives."},
        }
    elif aqi <= 300:
        insights["health"] = {
            "general": "Health alert: everyone may experience serious health effects.",
            "sensitive": "High risk for sensitive groups. Stay indoors and keep activity levels low.",
            "children": "Keep children indoors. Avoid all outdoor activities.",
            "elderly": "Elderly must stay indoors and rest. Avoid any exertion.",
            "asthma": "Dangerous for asthma patients. Stay indoors, use air purifiers, and monitor symptoms closely.",
        }
        insights["activities"] = {
            "walking": {"safe": False, "recommendation": "Avoid all outdoor walking. Stay indoors."},
            "running": {"safe": False, "recommendation": "Do not run outdoors. Dangerous conditions."},
            "outdoor_play": {"safe": False, "recommendation": "Absolutely no outdoor play. Children must stay indoors."},
            "cycling": {"safe": False, "recommendation": "Do not cycle outdoors."},
        }
    else:
        insights["health"] = {
            "general": "Health warnings of emergency conditions. Everyone is at risk.",
            "sensitive": "Extremely dangerous for sensitive groups. Remain indoors and minimize activity.",
            "children": "Keep children indoors with minimal activity. Close all windows.",
            "elderly": "Hazardous conditions. Elderly should remain indoors and rest.",
            "asthma": "Life-threatening for asthma patients. Stay indoors, use air purifiers, and seek medical advice if needed.",
        }
        insights["activities"] = {
            "walking": {"safe": False, "recommendation": "Hazardous. Do not go outdoors."},
            "running": {"safe": False, "recommendation": "Extremely dangerous. Do not go outdoors."},
            "outdoor_play": {"safe": False, "recommendation": "Emergency conditions. Keep everyone indoors."},
            "cycling": {"safe": False, "recommendation": "Hazardous. Do not go outdoors."},
        }

    return insights


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
