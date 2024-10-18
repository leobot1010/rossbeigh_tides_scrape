import requests
from bs4 import BeautifulSoup
from tides_send_email import send_email
import pandas as pd


""" ------------------------------------- GENERAL SCRAPING SETUP ---------------------------------------------- """

# add the user-agents and url to variables
agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/109.0.0.0 Safari/537.36"
}
url = "https://www.tideschart.com/Ireland/Munster/Kerry/Rossbeigh/"

# check for a response, we need a 200 response
response = requests.get(url, headers=agent)

# extract the html code
soup = BeautifulSoup(response.text, "lxml")


""" ------------------------------------------- TIDE TIMES ---------------------------------------------------"""

# extract the table from the webpage
table = soup.find("table", class_="table-xs table-striped w-100 h-100 tide-table")
# print(table)

# extract the line of code containing the headers
headers = table.find_all("th")

# extract all the titles, then extract first item, then extract the date from this
titles = [i.text for i in headers]
print(titles)
index_0 = titles[0]
today_date = index_0.split("Rossbeigh")[1]
print(today_date)


print(len(titles))

# extract high tide or low tide text headers. Some days there are only 3 tides.
first_tide_head = titles[4]
second_tide_head = titles[5]
third_tide_head = titles[6]
if len(titles) == 8:
    forth_tide_head = titles[7]
else:
    forth_tide_head = ''

# extract the times from the table
times = table.find_all("td")
tide_times = [i.text for i in times]

first_tide_value = tide_times[0]
second_tide_value = tide_times[2]
third_tide_value = tide_times[4]
if len(titles) == 8:
    forth_tide_value = tide_times[6]
else:
    forth_tide_value = ''
    # add one o

# Extract the sunset time
sun_table = soup.find("table", class_ = "table table-hover tidechart mb-4")
sun_times = sun_table.find_all("td", class_='sun')
sunset = sun_times[1].text[2:]


""" --------------------------------------------- WEATHER -----------------------------------------------------"""
# weather table is on a different page of the same website

agent_2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/109.0.0.0 Safari/537.36"
}
url_2 = "https://www.tideschart.com/Ireland/Munster/Kerry/Rossbeigh/Weather/"

response_2 = requests.get(url_2, headers=agent_2)

# extract the html code
soup_2 = BeautifulSoup(response_2.text, "lxml")

# extract the table from the webpage
weather_table = soup_2.find("table", class_="table table-striped table-hover mb-0")

table = soup.find("table", class_="table-xs table-striped w-100 h-100 tide-table")

w = weather_table.find_all("td")
w2 = [i.text for i in w]

w3 = []
for i in range(0, len(w2), 7):
    w3.append(w2[i:i+7])

print(w3[3])


""" ------------------------------------------ SEND EMAIL -------------------------------------------------------"""

email_text = f"""
Good Morning Kieran, here are the tides and weather for Rossbeigh beach for today {today_date}.

SUNSET: {sunset}

TIDES:
{first_tide_head:<12}{first_tide_value}
{second_tide_head:<12}{second_tide_value}
{third_tide_head:<12}{third_tide_value}
{forth_tide_head:<12}{forth_tide_value}

WEATHER:
{"09:00":<9}{w3[3][2]}   {w3[3][3]}
{"12:00":<9}{w3[4][2]}   {w3[4][3]}
{"15:00":<9}{w3[5][2]}   {w3[5][3]}
{"18:00":<9}{w3[6][2]}   {w3[6][3]}
{"21:00":<9}{w3[7][2]}   {w3[7][3]}
"""

send_email(email_text)
print(email_text)
