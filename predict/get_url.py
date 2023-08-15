import requests
from bs4 import BeautifulSoup
import re
import time
import csv

year_list = ["2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014"]


for year in year_list:
    time.sleep(2)
    race_list = []
    print(year)
    url = "https://db.netkeiba.com/?pid=race_list&word=&start_year="+year+"&start_mon=none&end_year="+year+"&end_mon=none&jyo%5B%5D=01&jyo%5B%5D=02&jyo%5B%5D=03&jyo%5B%5D=04&jyo%5B%5D=05&jyo%5B%5D=06&jyo%5B%5D=07&jyo%5B%5D=08&jyo%5B%5D=09&jyo%5B%5D=10&grade%5B%5D=1&grade%5B%5D=2&kyori_min=&kyori_max=&sort=date&list=100"
    request = requests.get(url)

    soup = BeautifulSoup(request.text, "html.parser")
    url_list = soup.find_all("a", attrs={"href": re.compile("^/race/\d+")})

    for url in url_list:
        race_list.append(url.get("href"))
    
    with open(year+'_url.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows([[url] for url in race_list])

