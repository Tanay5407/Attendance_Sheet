"""
# import module
from tabulate import tabulate

# assign data
mydata = [
	["Nikhil", "Delhi"], 
	["Ravi", "Kanpur"]
]

# create header
head = ["Name", "City"]

# display table
print(tabulate(mydata, headers=head, tablefmt="grid"))
"""

# import module
from tabulate import tabulate

# assign data
mydata = [
	['a', 'b', 'c'],
	[12, 34, 56],
	['Geeks', 'for', 'geeks!']
]

# display table
print(tabulate(mydata))
