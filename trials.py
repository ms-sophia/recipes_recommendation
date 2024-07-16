import requests
from bs4 import BeautifulSoup

# GET requests
r = requests.get("https://panlasangpinoy.com/categories/recipes/chicken-recipes/")

# determine the status code, 200 - success code
print(r.status_code)

# parse the html
soup = BeautifulSoup(r.content, "html.parser")
# print(soup.prettify)
# print(soup.title)
# print(soup.title.name)
# print(soup.title.parent.name)


s = soup.find("div", class_="site-inner")
# print(s)

lines = s.find_all("article")
# print(lines)

for line in lines:
    print(line.text)
# finding elements by id
# s = soup.find("div", id="genesis-content")
# print(s)
