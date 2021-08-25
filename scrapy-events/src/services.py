from typing import Dict
import datetime as _dt
import json as _json

def get_all_events() -> Dict:
    with open("events.json", encoding="utf-8") as events_file:
        return _json.load(events_file)


def get_month_events(month:str) -> Dict:
    events = get_all_events()
    try:
        return events[month.lower()]
    except KeyError:
        return "This month isn't real you fool"


def get_today():
    today = _dt.date.today()
    month = today.strftime("%B")
    day = today.day - 1
    return get_events_of_day(month, day)


def get_events_of_day(month:str, day:int) -> Dict:
    events = get_all_events()
    try:
        return events[month.lower()][str(day)]
    except KeyError:
        return "This day isn't real you fool"
