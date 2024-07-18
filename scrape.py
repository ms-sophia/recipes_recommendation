import urllib.request
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib
import csv
import time

pages_to_scrape = 200

recipes = []
urls = []
ingredients = []
string = []
cnt = 0
request_delay = 3
for page in range(1, pages_to_scrape + 1):

    # construct url
    url = "https://panlasangpinoy.com/recipes/page/" + str(page) + "/"
    r = requests.get(url)
    print(f"base url:{r.status_code} and count={cnt}")
    cnt = cnt + 1

    soup = BeautifulSoup(r.content, "html.parser")
    s = soup.find("div", class_="content-sidebar-wrap")
    lines = s.find_all("article", "category-recipes")

    try:
        for line in lines:
            link = line.find("a", "entry-title-link")
            recipes.append(line.text)
            urls.append(link.get("href"))

        # sleep to add a delay between requests
        time.sleep(request_delay)

    except requests.exceptions.RequestException as e:
        # Handle HTTP request errors (e.g connection issues)
        print(f"Error on page {page}: {e}")

    except IndexError as e:
        # Handle "list index out of range" error
        print(f"Index error on page {page}: {e}")

    except Exception as e:
        # Handle other unexpected errors
        print(f"Unxpected error on page {page}: {e}")


for url in urls:

    r = requests.get(url)
    print(f"recipe url:{r.status_code} and count={cnt}")
    cnt = cnt + 1
    soup = BeautifulSoup(r.content, "html.parser")
    s = soup.find("section", class_="oc-recipe-content")
    try:
        for ingredient in s.find_all("li", "wprm-recipe-ingredient"):
            ingredient = ingredient.text
            ingredient = ingredient.replace("▢ ", " ")  # remove checkbox
            string.append(ingredient)
        ingredients.append(",".join(string))
        string = []

        # sleep to add a delay between requests
        time.sleep(request_delay)

    except requests.exceptions.RequestException as e:
        # Handle HTTP request errors (e.g connection issues)
        print(f"Error on url {url}: {e}")

    except IndexError as e:
        # Handle "list index out of range" error
        print(f"Index error on url {url}: {e}")

    except Exception as e:
        # Handle other unexpected errors
        print(f"Unxpected error on url {url}: {e}")


df3 = pd.DataFrame(data={"names": recipes, "url": urls, "ingredients": ingredients})
print(df3)

df3.to_csv("rawData.csv", index=False)
