from prettytable import PrettyTable 

myTable = PrettyTable(["Student Name", "Class", "Section", "Percentage"]) 

myTable.add_row(["Leanord", "X", "B", "91.2 %"]) 
myTable.add_row(["Penny", "X", "C", "63.5 %"]) 
myTable.add_row(["Howard", "X", "A", "90.23 %"]) 
myTable.add_row(["Bernadette", "X", "D", "92.7 %"]) 
myTable.add_row(["Sheldon", "X", "A", "98.2 %"]) 
myTable.add_row(["Raj", "X", "B", "88.1 %"]) 
myTable.add_row(["Amy", "X", "B", "95.0 %"]) 

print(myTable)

"""
from prettytable import PrettyTable as pt
table_name = pt(list_of_headers)
table_name.add_row(list_of_raw_data)
print(table_name)
"""