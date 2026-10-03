# Daily Assistant Demo

This repository demonstrates a simple multi-agent daily assistant architecture built for local use.

## Overview

The workspace contains a main daily assistant and multiple specialized subagents:

- Weather agent: retrieves weather for a location
- News agent: retrieves top local news for a location
- Time checker agent: converts a time between source and destination time zones

The project is designed to support a parent agent that decides which subagent to use based on the user request.

## Repository structure

- `.github/copilot-instructions.md` — main instruction file for the daily assistant
- `weather-query-agent/` — weather subagent
- `top-news-query-agent/` — news subagent
- `time-checker-agent/` — time conversion subagent

## Agent responsibilities

### Main daily assistant
The main instruction file defines the parent agent behavior:
- interpret the request
- route weather queries to the weather subagent
- route news queries to the news subagent
- reject unsupported request types
- keep responses short and factual

### Weather subagent
Located in `weather-query-agent/`.

It answers weather questions for locations around the world using the Open-Meteo API.

Run it:

```bash
cd weather-query-agent
python3 main.py "weather in Bangkok"
```

### News subagent
Located in `top-news-query-agent/`.

It retrieves top headlines for a location using Google News RSS.

Run it:

```bash
cd top-news-query-agent
python3 main.py "top news in Singapore"
```

### Time checker subagent
Located in `time-checker-agent/`.

It converts a time from one timezone to another and prints:
- Time
- Source Timezone
- Destination Timezone

Run it:

```bash
cd time-checker-agent
python3 main.py "14:30" "Asia/Tokyo" "Asia/Singapore"
```

## Example usage

```bash
cd weather-query-agent
python3 main.py "weather in Tokyo"
```

```bash
cd top-news-query-agent
python3 main.py "top news in France"
```

```bash
cd time-checker-agent
python3 main.py "09:00" "UTC" "Europe/London"
```

## Notes

- The project intentionally uses public APIs and local scripts rather than hardcoded mock data.
- This repo is a simple prototype for demonstrating multi-agent routing in a local VS Code workspace.
- The main behavior is controlled by the repo-level Copilot instruction file and per-agent `AGENTS.md` files.
