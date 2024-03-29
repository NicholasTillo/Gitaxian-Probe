import requests
from bs4 import BeautifulSoup

URL = "https://edhrec.com/top/salt"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
job_elements = soup.find_all("div", class_="Card_container__Ng56K")
driver.find_element_by_xpath("here you put the code you copied for the button").click()
print(job_elements)
for i in job_elements:
    print(i)