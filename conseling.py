from DrissionPage import Chromium
from bs4 import BeautifulSoup
import json

browser = Chromium()
tab = browser.latest_tab

soup = BeautifulSoup('html.parser')

tab.get('https://www.schooldirectory.org/directory-category/top-schools/')

