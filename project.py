from bs4 import BeautifulSoup
from datetime import datetime

class Resort():
    def __init__(self, resort_name, website = None):
        self.resort_name = resort_name
        self.website = website
        
class OpenResort(Resort):
    def __init__(self, resort_name, website, lift_open, total_lift, snow_depth, snow_fall, snow_fall_time, surface_status, total_trails, open_trails):
        super().__init__(resort_name, website)
        self.total_lift = total_lift
        self.lift_open = lift_open
        self.snow_depth = snow_depth
        self.snow_fall = snow_fall
        self.snow_fall_time = snow_fall_time
        self.surface_status = surface_status
        self.total_trails = total_trails
        self.open_trails = open_trails
        
class ClosedResort(Resort):
    def __init__(self, resort_name, website, open_date):
        super().__init__(resort_name, website)
        self.open_date = open_date
        
        


file = open('snow_report.html')
html_text = file.read()
soup = BeautifulSoup(html_text, 'html.parser')
file.close()

################Extracting all open resorts###################
all_open = soup.find_all('div', class_="styles_outer__3Km0M")
name_list = []
updata_time = []
snow_fall = []
snow_fall_time = []
snow_depth = []
surface_status = []
open_trails = []
open_lifts = []
for resorts in all_open:
    name_list.append(resorts.contents[2].contents[0].contents[0].contents[0].contents[0])
    updata_time.append(resorts.contents[2].contents[0].contents[0].contents[1].contents[0])
    #Other info resorts.contents[2].contents[0].contents[1]
    snow_fall.append(resorts.contents[2].contents[0].contents[1].contents[0].contents[1].contents[0])
    snow_fall_time.append(resorts.contents[2].contents[0].contents[1].contents[0].contents[2].contents[0])
    snow_depth.append(resorts.contents[2].contents[0].contents[1].contents[1].contents[1].contents[0])
    surface_status.append(resorts.contents[2].contents[0].contents[1].contents[1].contents[2].contents[0])
    open_trails.append(resorts.contents[2].contents[0].contents[1].contents[2].contents[1].contents[0])
    open_lifts.append(resorts.contents[2].contents[0].contents[1].contents[3].contents[1].contents[0])
    

######################Extract all closed resorts####################################
all_closed = soup.find_all('div', class_="styles_box__3bpbO")
closed_resorts = []
open_dates = []
for resorts in all_closed:
    closed_resorts.append(resorts.contents[1].contents[0].contents[0])
    open_dates.append(resorts.contents[1].contents[1].contents[0])

website_list = len(name_list)*[None]
open_resort_list = []
closed_resort_list = []

########Data Processing###############

#########Open Resorts##################
for i in range(len(snow_fall)):
    snow_fall[i] = int(snow_fall[i].replace("\"",""))

total_lifts = []
for i in range(len(open_lifts)):
    two_num = open_lifts[i].split("/")
    open_lifts[i] = int(two_num[0])
    total_lifts.append(int(two_num[1]))

total_trails = []
for i in range(len(open_trails)):
    try:
        two_num = open_trails[i].split("/")
        open_trails[i] = int(two_num[0])
        total_trails.append(int(two_num[1]))
    except:
        open_trails[i] = None
        total_trails.append(None)

for i in range(len(updata_time)):
    updata_time[i] = int(updata_time[i].replace(" hours ago", ""))
    
for i in range(len(snow_fall_time)):
    if (snow_fall_time[i] == "Today"):
        datetime_object = datetime.strptime("Dec 5 2021", "%b %d %Y")
    else:
        datetime_object = datetime.strptime(snow_fall_time[i] + " 2021", "%b %d %Y")
    snow_fall_time[i] = datetime_object
    
for i in range(len(snow_depth)):
    snow_depth[i] = snow_depth[i].replace("\"", "")
    if ("-" in snow_depth[i]):
        two_num = snow_depth[i].split("-")
        snow_depth[i] = [int(two_num[0]), int(two_num[1])]
        if snow_depth[i][0] == snow_depth[i][1]:
            snow_depth[i] = snow_depth[i][0]
    else:
        snow_depth[i] = int(snow_depth[i])
        
###################Closed Resorts####################
for i in range(len(open_dates)):
    open_dates[i] = open_dates[i].replace("Opening ", "")
    datetime_object = datetime.strptime(open_dates[i], "%Y %b %d")
    open_dates[i] = datetime_object


print()