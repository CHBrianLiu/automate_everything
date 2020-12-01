from datetime import date

from notion.block import Block, BreadcrumbBlock, HeaderBlock, PageBlock


def monthly_page_factory(
    current_date: date, base_page: Block, title_format: str
) -> PageBlock:
    month_page = base_page.children.add_new(PageBlock)
    month_page.title = current_date.strftime(title_format)

    # Header 1: To-do list
    month_page.children.add_new(HeaderBlock).title = "Daily log"

    return month_page


def daily_page_factory(
    current_date: date, base_page: Block, title_format: str
) -> PageBlock:
    daily_page = base_page.children.add_new(PageBlock)
    daily_page.title = current_date.strftime(title_format)

    # Breadcrumb
    daily_page.children.add_new(BreadcrumbBlock)
    # Header 1: To-do list
    daily_page.children.add_new(HeaderBlock).title = "To-do"
    # Header 1: Meetings
    daily_page.children.add_new(HeaderBlock).title = "Meetings"
    # Header 1: Work log
    daily_page.children.add_new(HeaderBlock).title = "Work log"

    return daily_page
