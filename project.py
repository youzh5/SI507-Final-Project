from bs4 import BeautifulSoup
from datetime import datetime
import secrete
import requests
from requests.models import Response
import json

'''
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
'''        
        


file = open('snow_report.html')
html_text = file.read()
soup = BeautifulSoup(html_text, 'html.parser')
file.close()

################Extracting all open resorts###################
all_open = soup.find_all('div', class_="styles_outer__3Km0M")
name_list = []
update_time = []
snow_fall = []
snow_fall_time = []
snow_depth = []
surface_status = []
open_trails = []
open_lifts = []
for resorts in all_open:
    name_list.append(resorts.contents[2].contents[0].contents[0].contents[0].contents[0])
    update_time.append(resorts.contents[2].contents[0].contents[0].contents[1].contents[0])
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

for i in range(len(update_time)):
    update_time[i] = int(update_time[i].replace(" hours ago", ""))
    
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
    
    
    
#################################API PART##########################
###################################################################

def open_cache(file_name):
    try:
        file = open(file_name, 'r')
        dict_out = json.loads(file.read())
        file.close()
    except:
        dict_out = {}
    return dict_out

def caching(dict_in, file_name):
    dumped = json.dumps(dict_in)
    file = open(file_name, 'w')
    file.write(dumped)
    file.close()
    

def sudo_url(base_url, params):
    sudo_url = base_url + "&"
    for key in params.keys():
        if key != "key":
            sudo_url = sudo_url + (f'{key}={params[key]}&')
    return sudo_url

def make_request(base_url, params):
    response = requests.get(base_url, params=params)
    result = response.json()
    return result

def cache_control(base_url, params, cache_name="default_cache.json"):
    cache_dict = open_cache(cache_name)
    sudo_url_in = sudo_url(base_url, params)
    if sudo_url_in in cache_dict.keys():
        result = cache_dict[sudo_url_in]
    else:
        result = make_request(base_url, params)
        cache_dict[sudo_url_in] = result
    caching(cache_dict, cache_name)
    return result
    
    

base_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
params = {
    "fields": "formatted_address,name,rating,opening_hours,geometry",
    "input": "",
    "inputtype": "textquery",
    "contact": "website",
    "key": secrete.api_key
}


###################################DATA Presentation#############################
open_dict = {}

for i in range(len(name_list)):
    params["input"] = name_list[i]
    result = cache_control(base_url, params)
    local_dict = {}
    local_dict["location"] = result["candidates"][0]["geometry"]['location']
    local_dict["rating"] = result["candidates"][0]["rating"]
    local_dict["snow_fall"] = snow_fall[i]
    local_dict["snow_fall_time"] = snow_fall_time[i]
    local_dict["snow_depth"] = snow_depth[i]
    local_dict["surface_status"] = surface_status[i]
    local_dict["update_time"] = update_time[i]
    local_dict["total_lifts"] = total_lifts[i]
    local_dict["open_lifts"] = open_lifts[i]
    local_dict["total_trails"] = total_trails[i]
    local_dict["open_trails"] = open_trails[i]
    open_dict[name_list[i]] = local_dict

closed_dict = {}

for i in range(len(closed_resorts)):
    params["input"] = closed_resorts[i]
    result = cache_control(base_url, params)
    local_dict = {}
    local_dict["location"] = result["candidates"][0]["geometry"]['location']
    try:
        local_dict["rating"] = result["candidates"][0]["rating"]
    except:
        local_dict["rating"] = None
    local_dict["open_dates"] = open_dates[i]

######################Tree Construct#########################
class Node():
    def __init__(self, left = None, right = None, isQuestion = False, data = None, name = None):
        self.left = left
        self.right = right
        self.isQuestion = isQuestion
        self.data = data
        self.name = name
        
def questionEstablisher():
    ###################question nodes
    highest_rating = Node(isQuestion=True, data="Do you want to look for resort with the highest rating?[Y/N]")
    most_recent_snow = Node(isQuestion=True, data="Do you want to look for resort with the most snow fall?[Y/N]")
    most_lifts_open = Node(isQuestion=True, data="Do you want to look for resort with the most lifts open?[Y/N]")
    most_total_trails = Node(isQuestion=True, data="Do you want to look for resort with the most total trails?[Y/N]")
    more_snow = Node(isQuestion=True, data="Do you want to look for resort with the more snow depth?[Y/N]")
    
    #Data nodes
    nubs = Node(isQuestion=False, data=open_dict["Nubs Nob Ski Area"], name="Nubs Nob Ski Area")
    brule = Node(isQuestion=False, data=open_dict["Ski Brule"], name="Ski Brule")
    holly = Node(isQuestion=False, data=open_dict["Mount Holly"], name="Mount Holly")
    boyne = Node(isQuestion=False, data=open_dict["Boyne Mountain Resort"], name="Boyne Mountain Resort")
    brighton = Node(isQuestion=False, data=open_dict["Mt. Brighton"], name="Mt. Brighton")
    bsr = Node(isQuestion=False, data=open_dict["Big Snow Resort - Blackjack"], name="Big Snow Resort - Blackjack")
    
    #Constructing the tree
    highest_rating.left = nubs
    highest_rating.right = most_recent_snow
    most_recent_snow.left = brule
    most_recent_snow.right = most_lifts_open
    most_lifts_open.left = holly
    most_lifts_open.right = most_total_trails
    most_total_trails.left = boyne
    most_total_trails.right = more_snow
    more_snow.left = brighton
    more_snow.right = bsr
    
    current_node = highest_rating
    
    while current_node.isQuestion:
        answer = input(current_node.data)
        if (answer.lower() == 'y'):
            current_node = current_node.left
        elif (answer.lower() == 'n'):
            current_node = current_node.right
        else:
            print("This input is invalid. Please try again.")
            
    print(current_node.name)
        
questionEstablisher()
    

print()