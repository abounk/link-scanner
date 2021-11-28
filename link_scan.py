import os
import sys

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from typing import List
import requests

option = Options()
option.headless = True
browser = webdriver.Chrome(options=option)


def clear_link(url: str):
    """Remove page fragments (the '#' part) and query parameters
    (everything after “?”) from the url

    Args:
        url (str): a link.
    Returns:
        a url without fragments and query parameter.
    """
    link = url.split("#")
    link = link[0].split("?")
    return link[0]


def get_links(url: str):
    """Find all links on page at the given url.

    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """
    links = set()
    browser.get(url)
    elements: List[WebElement] = browser.find_elements(By.TAG_NAME, "a")
    for item in elements:
        href = item.get_attribute('href')
        if href:
            links.add(clear_link(href))
    return list(links)


def is_valid_url(url: str):
    """test if a url is valid & reachable or not.

    Args:
        url (str): a link.
    Returns:
        True if the URL is OK, False otherwise.
        Also return False is the URL has invalid syntax.
    """
    try:
        response = requests.head(url)
    except (requests.ConnectionError, requests.ConnectTimeout):
        return False
    if not response.ok:
        return False
    return True


def invalid_urls(urllist: List[str]) -> List[str]:
    """Validate the urls in urllist

    Args:
        urllist (list): list of urls.
    Retruns:
        a new list containing the invalid or
        unreachable urls.
    """
    bad_links = []
    for url in urllist:
        if not is_valid_url(url):
            bad_links.append(url)
    return bad_links


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        filename = os.path.basename(sys.argv[0])
        print(f"Usage: python3 {filename} url")
    url = args[1]
    links_from_url = get_links(url)
    for link in links_from_url:
        print(link)

    bad_links = invalid_urls(links_from_url)
    print()
    print("Bad Links:")
    for link in bad_links:
        print(link)
