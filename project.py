from bs4 import BeautifulSoup

file = open('snow_report.html')
html_text = file.read()
soup = BeautifulSoup(html_text, 'html.parser')

all_open = soup.find_all('div', class_="styles_outer__3Km0M")
name_list = []
updata_time = []
for resorts in all_open:
    name_list.append(resorts.contents[2].contents[0].contents[0].contents[0].contents[0])
    updata_time.append(resorts.contents[2].contents[0].contents[0].contents[1].contents[0])
    #Other info resorts.contents[2].contents[0].contents[1]

print(all_divs)