# Weather Query Agent

This project is a lightweight weather agent that answers location-based weather questions using the Open-Meteo public API.

## Features

- Accepts a natural-language weather query
- Resolves city names using geocoding
- Returns current weather and daily temperature range
- Runs as a CLI or interactive prompt

## Run it

From this folder:

python3 main.py "weather in Tokyo"

Or start an interactive session:

python3 main.py

## Example output

Current weather in Tokyo, Japan: Mostly clear. Temperature is 21.3°C with a feels-like of 20.9°C. Wind speed is 8.0 km/h and precipitation is 0.0 mm. Today's expected range is 18.0°C to 25.0°C.
