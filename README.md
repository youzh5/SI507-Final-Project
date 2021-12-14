# This project is for final project of SI507 @ University of Michigan  
A Google cloud API key is required to run the program.  
The api key should be saved in secrete.py and named as api_key = "xxxxxxx".  
Put secrete.py in the same folder as project.py and run. The user will be prompted.  
Make sure the program has the permission to write.  
Data cache is uploaded to demonstrate the caching for checkpoint; it can be removed  
### Proper GUI or graphic forwarding for python is required to show the map (as png).  
  
### Tree structure  
The data are placed in the node. The node object has left, right, data, name and a boolean  
as its variables. The left and right variable will point to the next node. The data will either  
be a question string or the information of a resort. The name variable will store the name  
if the node is a resort. isQuestion determines either a node is a question or resort node.  
The tree is constructed so that questions will be asked until a resort node is reached.  
Answer yes will point to the left of the branch and answer no will point to the right.