#!/usr/bin/env python3
import argparse
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

COMMON_TIMEZONES = {
    "UTC": timezone.utc,
    "Asia/Tokyo": timezone(timedelta(hours=9)),
    "Asia/Singapore": timezone(timedelta(hours=8)),
    "Asia/Hong_Kong": timezone(timedelta(hours=8)),
    "Asia/Bangkok": timezone(timedelta(hours=7)),
    "Asia/Shanghai": timezone(timedelta(hours=8)),
    "Asia/Kuala_Lumpur": timezone(timedelta(hours=8)),
    "Asia/Manila": timezone(timedelta(hours=8)),
    "Asia/Sydney": timezone(timedelta(hours=10)),
    "Asia/Kolkata": timezone(timedelta(hours=5, minutes=30)),
    "Asia/Dubai": timezone(timedelta(hours=4)),
    "Asia/Taipei": timezone(timedelta(hours=8)),
    "Asia/Seoul": timezone(timedelta(hours=9)),
    "Asia/Tashkent": timezone(timedelta(hours=5)),
    "Asia/Phnom_Penh": timezone(timedelta(hours=7)),
    "Asia/Vientiane": timezone(timedelta(hours=7)),
    "Asia/Jakarta": timezone(timedelta(hours=7)),
    "Asia/Ho_Chi_Minh_City": timezone(timedelta(hours=7)),
}


def parse_time(value):
    try:
        return datetime.strptime(value, "%H:%M")
    except ValueError:
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Please provide a valid time in HH:MM format, e.g. 14:30")


def normalize_timezone(value):
    if not value or not value.strip():
        raise ValueError("Please provide a timezone name, such as Asia/Tokyo or UTC.")
    key = value.strip()
    if key in COMMON_TIMEZONES:
        return COMMON_TIMEZONES[key]
    try:
        return ZoneInfo(key)
    except Exception as exc:
        normalized = key.replace(" ", "_")
        if normalized in COMMON_TIMEZONES:
            return COMMON_TIMEZONES[normalized]
        raise ValueError(f"Unsupported timezone: {value}") from exc


def convert_time(source_time, source_tz, target_tz):
    source_dt = datetime.combine(datetime.today().date(), parse_time(source_time).time())
    source_dt = source_dt.replace(tzinfo=source_tz)
    target_dt = source_dt.astimezone(target_tz)
    return target_dt


def format_response(source_time, source_tz, target_tz):
    target_time_obj = convert_time(source_time, source_tz, target_tz)
    return (
        f"Time: {target_time_obj.strftime('%H:%M')}\n"
        f"Source Timezone: {source_tz}\n"
        f"Destination Timezone: {target_tz}"
    )


def main():
    parser = argparse.ArgumentParser(description="Convert a time from one timezone to another.")
    parser.add_argument("source_time", help="Example: 14:30")
    parser.add_argument("source_timezone", help="Example: Asia/Tokyo")
    parser.add_argument("target_timezone", help="Example: Asia/Singapore")
    args = parser.parse_args()

    try:
        source_tz = normalize_timezone(args.source_timezone)
        target_tz = normalize_timezone(args.target_timezone)
        print(format_response(args.source_time, source_tz, target_tz))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
