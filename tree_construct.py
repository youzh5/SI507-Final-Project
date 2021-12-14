import json

class Node():
    def __init__(self, left = None, right = None, isQuestion = False, data = None, name = None):
        self.left = left
        self.right = right
        self.isQuestion = isQuestion
        self.data = data
        self.name = name

file = open("open_cach.json", 'r')
open_dict = json.loads(file.read())
file.close()


highest_rating  = Node(isQuestion=True, data="Do you want to look for resort with the highest rating?[Y/N]", name="rating question")
most_recent_snow = Node(isQuestion=True, data="Do you want to look for resort with the most snow fall?[Y/N]", name = "recent snow question")
most_lifts_open = Node(isQuestion=True, data="Do you want to look for resort with the most lifts open?[Y/N]", name = "lift question")
most_total_trails = Node(isQuestion=True, data="Do you want to look for resort with the most total trails?[Y/N]", name = "trail question")
more_snow = Node(isQuestion=True, data="Do you want to look for resort with the more snow depth?[Y/N]", name = "snow depth question")

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
most_recent_snow.left = more_snow
most_recent_snow.right = most_lifts_open
most_lifts_open.left = holly
most_lifts_open.right = most_total_trails
most_total_trails.left = boyne
most_total_trails.right = brighton
more_snow.left = brule
more_snow.right = bsr

nodes = [highest_rating, most_recent_snow, most_lifts_open, most_total_trails, more_snow, nubs, brule, holly, boyne, brighton, bsr]

jdict = {}
for node in nodes:
    try: 
        jdict.update({node.name: {"left": node.left.name, "right": node.right.name, "isQuestion": str(node.isQuestion), "data": node.data}})
    except:
        jdict.update({node.name: {"left": "None", "right": "None", "isQuestion": str(node.isQuestion), "data": node.data}})
    
dumped = json.dumps(jdict)
file = open("tree_dict.json", 'w')
file.write(dumped)
file.close()






'''
Tree Stucture:

       Q:rating
    /            \ 
 R: Nubs        Q:recent snow
                /         \ 
            Q:snow depth    Q: most lifts
            /       \           /     \ 
          brule     bsr       Holly   Q: total trails
                                          /      \ 
                                        Boyne    Brighton
'''