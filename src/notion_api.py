#!/usr/bin/env -S PATH="${PATH}:/usr/local/bin" python3

# Heavily borrowed from https://github.com/kevinjalbert/alfred-notion/blob/v1.0.0/src/notion_api.py
# TODO: Would be nice to replace this and the source material with a common package

from cachetools import cached
from datetime import datetime

from notion.client import NotionClient
from notion.block import DividerBlock, TextBlock

from config import notionToken, tasksDatabaseURL, yearPageURL


@cached(cache={})
def client():
    return NotionClient(token_v2=notionToken(), monitor=False)


@cached(cache={})
def tasksDatabase():
    return client().get_collection_view(tasksDatabaseURL())


@cached(cache={})
def currentYear():
    return client().get_block(yearPageURL())


@cached(cache={})
def currentWeek():
    currentWeek = None
    currentDate = datetime.now()

    # Sunday Starts the week
    weekNumber = str(currentDate.isocalendar()[
                     1] + (currentDate.isoweekday() == 7))

    for weekPage in currentYear().children:
        if weekPage.title.startswith("Week " + weekNumber):
            currentWeek = weekPage
            break
        else:
            next

    return currentWeek


@cached(cache={})
def currentDay():
    currentDay = None
    currentDate = datetime.now()

    dayNumber = str(currentDate.day)
    monthName = currentDate.strftime("%B")
    daysPage = currentWeek().children[1].children[1]

    for dayPage in daysPage.children:
        if dayPage.title.startswith(monthName + " " + dayNumber):
            currentDay = dayPage
            break
        else:
            next

    return currentDay


def appendToCurrentDayNotes(content):
    # Get the divider block that signifies the end of the notes for the current day
    dividerBlock = [x for x in currentDay().children if type(x)
                    == DividerBlock][0]

    # Add note to end of the page, then move it to before the divider
    noteBlock = currentDay().children.add_new(TextBlock, title=content)
    noteBlock.move_to(dividerBlock, "before")

    return noteBlock
