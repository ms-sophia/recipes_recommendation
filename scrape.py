import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

recipes = []
urls = []
ingredients = []
string = []
request_delay = 3
urls_ingri = []
pages_to_scrape = 100


def scrape_ingri(url):
    global string
    try:
        r = requests.get(url)
        url_text = url.split("/")
        print(f"recipe url:{r.status_code} {url_text[3]}")
        # soup = BeautifulSoup(r.content, "lxml")
        soup = BeautifulSoup(r.content, "html.parser")
        s = soup.find("section", class_="oc-recipe-content")

        # check for server errors or maintenance
        if soup.title and "service unavailable" in soup.title.text.lower():
            print(f"Server error on page {url} Skipping...")
            print(f"deleting the name and url")
            del recipes[-1]
            del url[-1]
            return 0

        for ingredient in s.find_all("li", "wprm-recipe-ingredient"):
            ingredient = ingredient.text
            ingredient = ingredient.replace("▢ ", "")  # remove checkbox
            ingredient = ingredient.replace("\n", "")
            string.append(ingredient)
        # print(string)
        ingredients.append(string)
        urls_ingri.append(url_text[3])
        string = []
        # sleep to add a delay between requests
        time.sleep(request_delay)

    except requests.exceptions.RequestException as e:
        # Handle HTTP request errors (e.g connection issues)
        print(f"Error on url {url}: {e}")
        # delete url and names
        print(f"deleting the name and url")
        del recipes[-1]
        del urls[-1]

    except IndexError as e:
        # Handle "list index out of range" error
        print(f"Index error on url {url}: {e}")
        # delete url and names
        print(f"deleting the name and url")
        del recipes[-1]
        del urls[-1]

    except Exception as e:
        # Handle other unexpected errors
        print(f"Unxpected error on url {url}: {e}")
        # delete url and names
        print(f"deleting the name and url")
        del recipes[-1]
        del urls[-1]

    df = pd.DataFrame(data={"names": recipes, "url": urls, "ingredients": ingredients})
    # df2 = pd.DataFrame(data={"ingredients": ingredients, "url": urls_ingri})
    # df = df.explode("ingredients")
    df.to_csv("data.csv", index=False)
    # df2.to_csv("ingri_data.csv", index=False)

    return 0


def scrape():
    for page in range(1, pages_to_scrape + 1):

        try:
            # construct url
            url = f"https://panlasangpinoy.com/recipes/page/{page}/"
            r = requests.get(url)
            print(f"base url:{r.status_code} and page: {page}")
            soup = BeautifulSoup(r.content, "html.parser")
            # soup = BeautifulSoup(r.content, "lxml")

            s = soup.find("div", class_="content-sidebar-wrap")
            lines = s.find_all("article", "category-recipes")

            # check for server errors or maintenance
            if soup.title and "service unavailable" in soup.title.text.lower():
                print(f"Server error on page {page} Skipping...")
                continue

            for line in lines:
                link = line.find("a", "entry-title-link")
                line = line.text
                line = line.replace("\n", "")
                print(line)
                recipes.append(line)
                url = link.get("href")
                urls.append(url)
                scrape_ingri(url)

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

    # df1 = pd.DataFrame(data={"names": recipes, "url": urls})
    # df1.to_csv("names_url_data.csv", index=False)
    df1 = pd.DataFrame(data={"names": recipes, "url": urls, "ingredients": ingredients})
    df1.to_csv("data.csv", index=False)
