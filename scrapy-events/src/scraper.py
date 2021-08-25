from typing import List

import requests as _requests
import bs4 as _bs4

def _genrate_url(month:str, day:int) -> str:
    url = f"https://www.onthisday.com/day/{month}/{day}"
    return url

def _get_page(url:str) -> _bs4.BeautifulSoup:
    page = _requests.get(url)
    soup = _bs4.BeautifulSoup(page.content, "html.parser")
    return soup

def events_of_the_day(month:str, day:int) -> List:
    url = _genrate_url(month, day)
    page = _get_page(url)
    row_events = page.find_all(class_="event")
    events = [event.text for event in row_events]
    return events
