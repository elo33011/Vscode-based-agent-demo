#!/usr/bin/env python3
import argparse
import re
import sys
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

RSS_URL = "https://news.google.com/rss/search"


def normalize_query(query):
    cleaned = (query or "").strip()
    if not cleaned:
        return ""
    cleaned = re.sub(r"^(what|what's|tell me|show me|give me|top|latest)\s+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^(news|headlines)\s+(for|in|at|around|near)\s+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^(for|in|at|around|near)\s+", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+news\s*$", "", cleaned, flags=re.IGNORECASE)
    cleaned = cleaned.strip(" ?!.,")
    return cleaned


def fetch_news_feed(location):
    if not location:
        raise ValueError("Please provide a location such as 'top news in London'.")

    query = quote_plus(f"{location} news")
    url = f"{RSS_URL}?q={query}&hl=en-US&gl=US&ceid=US:en"
    request = Request(url, headers={"User-Agent": "top-news-query-agent/1.0"})
    with urlopen(request, timeout=20) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    items = root.findall("./channel/item")
    if not items:
        raise ValueError(f"No news items were found for '{location}'.")
    return items


def summarize_news(location, items, limit=5):
    print(f"Top news for {location}:")
    for index, item in enumerate(items[:limit], start=1):
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        pub_date = item.findtext("pubDate", "").strip()
        description = item.findtext("description", "").strip()

        print(f"{index}. {title}")
        if pub_date:
            print(f"   Published: {pub_date}")
        if link:
            print(f"   Link: {link}")
        if description:
            short_desc = re.sub(r"<.*?>", "", description)
            short_desc = re.sub(r"\s+", " ", short_desc).strip()
            if short_desc:
                print(f"   Summary: {short_desc[:180]}" + ("..." if len(short_desc) > 180 else ""))
        print()


def answer_news_query(query):
    location = normalize_query(query)
    items = fetch_news_feed(location)
    summarize_news(location, items)


def interactive_loop():
    print("Top News Query Agent")
    print("Type 'quit' to exit.")
    while True:
        try:
            raw = input("Ask for top news by location: ").strip()
        except EOFError:
            print()
            break

        if raw.lower() in {"quit", "exit", "q"}:
            print("Goodbye.")
            break

        try:
            answer_news_query(raw)
        except Exception as exc:
            print(f"I could not answer that: {exc}")


def main():
    parser = argparse.ArgumentParser(description="Get top local news for a location.")
    parser.add_argument("query", nargs="?", help="Example: 'top news in Paris'")
    args = parser.parse_args()

    if args.query:
        try:
            answer_news_query(args.query)
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        interactive_loop()


if __name__ == "__main__":
    main()
