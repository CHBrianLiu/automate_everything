import configparser
import logging
import os
from datetime import date

import azure.functions as func
from notion.client import NotionClient

from .factory import daily_page_factory, monthly_page_factory


def main(mytimer: func.TimerRequest) -> None:
    # load config
    logging.debug("Load config...")
    page_settings_file = os.path.join(os.path.dirname(__file__), "page.ini")
    if not os.path.exists(page_settings_file):
        logging.error("File not exists. %s", page_settings_file)
        raise FileNotFoundError
    page_settings = configparser.ConfigParser()
    page_settings.read(page_settings_file)

    # Retrieve config
    month_page_title_format = page_settings["TitleFormat"]["MONTH_PAGE_TITLE_FORMAT"]
    daily_page_title_format = page_settings["TitleFormat"]["DAIYLY_PAGE_TITLE_FORMAT"]
    startup_page_title = page_settings["Home"]["PAGE_TITLE"]

    # Create Notion session
    client = NotionClient(token_v2=os.environ["USER_TOKEN"])

    # Access the startup page
    startup_page = None
    for page in client.get_top_level_pages():
        if page.title == startup_page_title:
            startup_page = page

    # Retrieve date info
    today = date.today()
    month_page_title = today.strftime(month_page_title_format)
    daily_page_title = today.strftime(daily_page_title_format)

    # Check month page existance.
    month_page = None
    for child in startup_page.children:
        if child.title == month_page_title:
            month_page = child
    if month_page is None:
        # Create month page
        month_page = monthly_page_factory(
            current_date=today,
            base_page=startup_page,
            title_format=month_page_title_format,
        )

    # Check daily page existance.
    daily_page = None
    for child in month_page.children:
        if child.title == daily_page_title:
            month_page = child
    if daily_page is None:
        # Create daily page
        daily_page_factory(
            current_date=today,
            base_page=month_page,
            title_format=daily_page_title_format,
        )
