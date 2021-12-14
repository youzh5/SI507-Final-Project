import json
import pprint

file = open("tree_dict.json", 'r')
tree_dict = json.loads(file.read())
file.close()

pprint.pprint(tree_dict)