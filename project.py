from bs4 import BeautifulSoup
from datetime import datetime
import secrete
import requests
from requests.models import Response
import json
from PIL import Image
import pprint

'''
This program is for the user to check snow status.
The program will display location and name of the resort by the user's preference.
All data are scraped on Dec 5th, therefore, all comparison will be based on this date
'''        
        
    
    
    
#################################API PART##########################
###################################################################

#open cache
def open_cache(file_name):
    try:
        file = open(file_name, 'r')
        dict_out = json.loads(file.read())
        file.close()
    except:
        dict_out = {}
    return dict_out

#save cache
def caching(dict_in, file_name):
    dumped = json.dumps(dict_in)
    file = open(file_name, 'w')
    file.write(dumped)
    file.close()
    
#construct unique sudo url
def sudo_url(base_url, params):
    sudo_url = base_url + "&"
    for key in params.keys():
        if key != "key":
            sudo_url = sudo_url + (f'{key}={params[key]}&')
    return sudo_url

#make request
def make_request(base_url, params):
    response = requests.get(base_url, params=params)
    result = response.json()
    return result

#open cache and check if request in cache
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


#########NODES and Trees############
##########For data presentation#############
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
            
    return current_node


########The final presentation, shows the map##########
'''
    NOTE: This requires GUI/graphics forwarding
    Tested on author's windows10 python 3.7.2 environment and passed
'''
        
def getMap(resorts):
    map_base_url = "https://maps.googleapis.com/maps/api/staticmap"
    map_params = {
        "center": "Traverse+City",
        "zoom": "6",
        "size": "1200x1200",
        "maptype": "roadmap",
        "key": secrete.api_key,
        "markers": []
    }

    # if isOpen:
    #     for resort in resorts:
    #         map_params["markers"].append(str(open_dict[resort]["location"]["lat"]) + "," \
    #             + str(open_dict[resort]["location"]["lng"]))
    # else:
    #     for resort in resorts:
    #         map_params["markers"].append(str(closed_dict[resort]["location"]["lat"]) + "," \
    #             + str(closed_dict[resort]["location"]["lng"]))
    
    total_dict = {}
    total_dict.update(open_dict)
    total_dict.update(closed_dict)
    for resort in resorts:
        map_params["markers"].append(str(total_dict[resort]["location"]["lat"]) + "," \
            + str(total_dict[resort]["location"]["lng"]))
    
    # map_params["markers"] = [str(open_dict["Boyne Mountain Resort"]["location"]["lat"]) + "," + str(open_dict["Boyne Mountain Resort"]["location"]["lng"]), \
    #     str(open_dict["Ski Brule"]["location"]["lat"]) + "," + str(open_dict["Ski Brule"]["location"]["lng"])]

    response = requests.get(map_base_url, map_params)
    open("maps_temp.png", "wb").write(response.content)
    im = Image.open("maps_temp.png","r")
    im.show()


#############The main program of the file################
if __name__ == '__main__':
    #read the html file
    file = open('snow_report.html','rb')
    html_text = file.read().decode('utf8')
    soup = BeautifulSoup(html_text, 'html.parser')
    file.close()

    ################Extracting all open resorts###################
    #page scraping
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
        
    #page scraping COMPLETE
    
    
    
    base_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
    params = {
        "fields": "formatted_address,name,rating,opening_hours,geometry",
        "input": "",
        "inputtype": "textquery",
        "key": secrete.api_key
    }


    ###################################DATA Processing#############################
    
    #####Data process
    #processing open resorts data
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

    #processing closed resorts data
    closed_dict = {}

    for i in range(len(closed_resorts)):
        params["input"] = closed_resorts[i] + " Michigan"
        result = cache_control(base_url, params)
        local_dict = {}
        local_dict["location"] = result["candidates"][0]["geometry"]['location']
        try:
            local_dict["rating"] = result["candidates"][0]["rating"]
        except:
            local_dict["rating"] = 0
        local_dict["open_dates"] = open_dates[i]
        closed_dict[closed_resorts[i]] = local_dict
        
    #data processing COMPLETE
    
    ###########DATA presentation###########
    total_dict = {}
    total_dict.update(open_dict)
    total_dict.update(closed_dict)
    total_list = [(k, v) for k, v in total_dict.items()]
    
    ######bubble sort acording to the ratings#####
    for pass_num in range(len(total_list)-1, 0, -1):
        for i in range(pass_num):
            if (total_list[i][1]["rating"] < total_list[i+1][1]["rating"]):
                temp = total_list[i]
                total_list[i] = total_list[i+1]
                total_list[i+1] = temp
    
    highest_rating = [name for name, data in total_list][0:5]
    
    ########Find close resorts that will be open in 10 days#########
    def lookAhead(day):
        today = datetime.strptime("Dec 5 2021", "%b %d %Y")
        filtered = []
        standard = 60*24*int(day) #10 days to minutes
        for k, v in closed_dict.items():
            if (v["open_dates"] - today).total_seconds()/60 < standard:
                filtered.append(k)
        return filtered
    ########Find closest open resort#####################
    def find_closesest(zip):
        closest = list(open_dict.keys())[0]
        base_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json'
        params = {
            "fields": "formatted_address,name,rating,opening_hours,geometry",
            "input": zip,
            "inputtype": "textquery",
            "key": secrete.api_key
        }
        result = cache_control(base_url, params)
        location = result["candidates"][0]["geometry"]['location']
        min_dis = 1024 #fake distance
        for k, v in open_dict.items():
            lat_diff = location["lat"] - v["location"]["lat"]
            lng_diff = location["lng"] - v["location"]["lng"]
            dis = lat_diff**2 + lng_diff**2
            if dis < min_dis:
                min_dis = dis
                closest = k
        return closest
    
    ###############Qeustion Tree Recommendation############
    #######Please refer to the question tree function######
    
    ##############Main Program################
    started = False
    while True:
        print()
        if not started:
            print("It's time for snow season! I got some information of ski resorts in Michigan for you.")
            print("Please choose mode:")
            print()
            print("1. Show resorts with the highest ratings in Michigan")
            print("2. Show the closed resorts that will open in the next choosing number of days")
            print("3. Find the closes resort")
            print("4. I need som recommendation")
            print("5. I want to check more specific info")
            print()
        user_in = input("Please enter mode number or type \"exit\":    ")
        print()
        started = True
        if user_in == "1":
            print(f'The resorts with highest ratings are {highest_rating}. Showing them in the map.')
            getMap(highest_rating)
        elif user_in == "2":
            day = input("In how many days do you want to look for?    ")
            if day.isdigit():
                filtered = lookAhead(day)
                if len(filtered) != 0:
                    print(f'The resorts are going to be open in the next {day} days are {filtered}')
                    print("Showing locations on the map.")
                    getMap(filtered)
                else:
                    print("No resort found. Please try again.")
            else:
                print("This input is not valid. Please try again.")
        elif user_in == "3":
            addr = input("Please type in your address:  ")
            closest = find_closesest(addr)
            print(f'The resort closes to you is {closest}')
            print("Showing location on the map.")
            getMap([closest])
        elif user_in == "4":
            print("Recommendation process initiated!")
            name = questionEstablisher()
            print(f'You might like {name.name}!')
            getMap([name.name])
        elif user_in.lower() == "exit":
            print("Bye! Thanks for using!")
            break
        elif user_in == '5':
            while True:
                found = False
                name = input("Please type in a name for more info or type \"exit\":    ")
                if name.lower() == "exit":
                    break
                for k, v in total_dict.items():
                    if name.lower() == k.lower():
                        pprint.pprint(v)
                        print("Showing location on the map.")
                        getMap([k])
                        found = True
                if not found:
                    print("This resort is not found in the database. Please try again.")
        else:
            print("This input is illegal. Please try again.")
            
            
    ##########Dump the open_dict so that the info can be used in seperate tree file
    for k, v in open_dict.items():
        v["snow_fall_time"] = v["snow_fall_time"].strftime("%m/%d/%y")
    dumped = json.dumps(open_dict)
    file = open("open_cach.json", 'w')
    file.write(dumped)
    file.close()