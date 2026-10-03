#!/usr/bin/env python3
import argparse
import json
import re
import sys
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mostly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Freezing drizzle",
    57: "Heavy freezing drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Light rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Light snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Severe thunderstorm with hail",
}


def read_json(url):
    request = Request(url, headers={"User-Agent": "weather-query-agent/1.0"})
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def parse_location(query):
    cleaned = query.strip()
    if not cleaned:
        return ""

    cleaned = re.sub(r"^(what is|what's|tell me|please|can you)\s+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^(weather|forecast)\s+(in|at|for)\s+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^(in|at|for)\s+", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip(" ?!.,")
    return cleaned


def geocode_city(city_name):
    if not city_name:
        raise ValueError("Please provide a city name.")

    encoded_name = quote_plus(city_name)
    url = f"{GEOCODING_URL}?name={encoded_name}&count=1&language=en&format=json"
    data = read_json(url)
    results = data.get("results") or []
    if not results:
        raise ValueError(f"No weather data found for '{city_name}'.")

    result = results[0]
    return {
        "city": result.get("name", city_name),
        "region": result.get("admin1") or result.get("country") or "",
        "country": result.get("country", ""),
        "latitude": result["latitude"],
        "longitude": result["longitude"],
    }


def get_weather(latitude, longitude):
    params = (
        f"latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m"
        "&daily=temperature_2m_max,temperature_2m_min"
        "&timezone=auto&forecast_days=3"
    )
    url = f"{FORECAST_URL}?{params}"
    data = read_json(url)
    current = data.get("current") or {}
    daily = data.get("daily") or {}

    if not current:
        raise ValueError("Weather service did not return current conditions.")

    return {
        "temperature": current.get("temperature_2m"),
        "feels_like": current.get("apparent_temperature"),
        "precipitation": current.get("precipitation"),
        "wind_speed": current.get("wind_speed_10m"),
        "weather_code": current.get("weather_code"),
        "high": (daily.get("temperature_2m_max") or [None])[0],
        "low": (daily.get("temperature_2m_min") or [None])[0],
    }


def describe_weather(code):
    return WEATHER_CODES.get(code, "Variable conditions")


def build_summary(city, region, country, weather):
    temp = weather["temperature"]
    feels_like = weather["feels_like"]
    precipitation = weather["precipitation"]
    wind_speed = weather["wind_speed"]
    code = weather["weather_code"]
    high = weather["high"]
    low = weather["low"]

    location = city
    if region and region.lower() != city.lower() and region != country:
        location = f"{city}, {region}"
    if country:
        location = f"{location}, {country}"

    return (
        f"Current weather in {location}: {describe_weather(code)}. "
        f"Temperature is {temp}°C with a feels-like of {feels_like}°C. "
        f"Wind speed is {wind_speed} km/h and precipitation is {precipitation} mm. "
        f"Today's expected range is {low}°C to {high}°C."
    )


def answer_weather_query(query):
    city_query = parse_location(query)
    if not city_query:
        raise ValueError("Please enter a location such as 'weather in Tokyo'.")

    location = geocode_city(city_query)
    weather = get_weather(location["latitude"], location["longitude"])
    return build_summary(location["city"], location["region"], location["country"], weather)


def interactive_loop():
    print("Weather Query Agent")
    print("Type 'quit' to exit.")
    while True:
        try:
            raw = input("Ask about the weather: ").strip()
        except EOFError:
            print()
            break

        if raw.lower() in {"quit", "exit", "q"}:
            print("Goodbye.")
            break

        try:
            print(answer_weather_query(raw))
        except Exception as exc:  # pragma: no cover - user-facing fallback
            print(f"I could not answer that: {exc}")


def main():
    parser = argparse.ArgumentParser(description="Query a weather forecast for a city.")
    parser.add_argument("query", nargs="?", help="Example: 'weather in Tokyo'")
    args = parser.parse_args()

    if args.query:
        try:
            print(answer_weather_query(args.query))
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        interactive_loop()


if __name__ == "__main__":
    main()
