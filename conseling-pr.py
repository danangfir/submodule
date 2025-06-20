from patchright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import csv

contact = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.schooldirectory.org/directory-category/top-schools/")
    content = page.content()
    soup = BeautifulSoup(content, "html.padrser")