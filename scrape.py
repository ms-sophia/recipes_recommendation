import requests
from bs4 import BeautifulSoup
import pandas as pd

# # GET request
# r = requests.get("https://panlasangpinoy.com/recipes/page/1/")

# # check if sucess in GET
# print(r.status_code)

pages_to_scrape = 2

recipe = []
urls = []
ingredients = []

for page in range(1, pages_to_scrape + 1):

    # construct url
    url = "https://panlasangpinoy.com/recipes/page/" + str(page) + "/"
    r = requests.get(url)
    print(r.status_code)
    soup = BeautifulSoup(r.content, "html.parser")
    s = soup.find("div", class_="content-sidebar-wrap")
    lines = s.find_all("article")

    for line in lines:
        recipe.append(line.text)

    for link in s.find_all("a", "entry-image-link"):
        urls.append((link.get("href")))


df = pd.DataFrame(data={"names": recipe, "url": urls})
print(df)
