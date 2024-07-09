#including libraries
import mysql.connector as ms
import datetime as dt
import inquirer
import typer

#-----> Date and time
day = dt.datetime.today().day
month = dt.datetime.today().month
year = dt.datetime.today().year
print(f"Day : {day}, month : {month}, year : {year}")
leap = False
if year % 4 == 0 and year % 400 != 0:
    leap = True

#-----> SQL Connection
conn = ms.connect(host="localhost", user="root", password="root")
cursor = conn.cursor()

#-----> Database Creation
database_name = "Attendance_Records".lower()
database_creation_query = f"create database if not exists {database_name};"
cursor.execute(database_creation_query)
cursor.execute(f"use {database_name}")
print(f"Database Created : {database_name}")

#-----> Table creation
table_name = "Names".lower()
table_creation_query = f"create table if not exists {table_name} (Admin VARCHAR(10) PRIMARY KEY, Name VARCHAR(20), Surname VARCHAR(20), Class VARCHAR(5), Section VARCHAR(2));"
cursor.execute(table_creation_query)
print(f"Table Created : {table_name}")

for i in range(1,13):
    table_name = f"{i}_{year}"
    command = f"CREATE TABLE IF NOT EXISTS {table_name} (Admin VARCHAR(10),"
    if i in [1,3,5,7,8,10,12]:
        for j in range(1,32):
            command = command + f"`{j}` VARCHAR(3) DEFAULT NULL, "
    if i in [4,6,9,11]:
        for j in range(1,31):
            command = command + f"`{j}` VARCHAR(3) DEFAULT NULL, "
    if i == 2:
        if leap == True:
            for j in range(1,30):
                command = command + f"`{j}` VARCHAR(3) DEFAULT NULL, "
        if leap == False:
            for j in range(1,29):
                command = command + f"`{j}` VARCHAR(3) DEFAULT NULL, "
    command = command[:-2]
    command = command + ");"
    print(command)
    print()
    cursor.execute(command)
print("Tables Created Successfully")

def add_student_names(parent):
    """Function which enables us to add students names and details to the database"""
    confirm  = inquirer.list_input("Sure?" ,choices = ["Yes", "Nope"])
    function = globals()[parent]
    if confirm == "Nope":
        function()
    elif confirm == "Yes":
        Admin = typer.prompt("Enter Admin Number")
        Name = typer.prompt("Enter Name")
        Surname = typer.prompt("Enter Surname")
        Class = typer.prompt("Enter Class")
        Section = typer.prompt("Enter Section")

        insert_query = "INSERT INTO names(Admin, Name, Surname, Class, Section) values(%s, %s, %s, %s, %s);"
        arg = (Admin, Name, Surname, Class, Section)
        print(insert_query, arg)
        cursor.execute(insert_query, arg)
        conn.commit()
        print(function)
        function()

def enter_attendance_records(parent):
    confirm  = inquirer.list_input("Sure?" ,choices = ["Yes", "Nope"])
    function = globals()[parent]
    if confirm == "Nope":
        function()
    elif confirm == "Yes":
        checkboxQuestion = [
                inquirer.Checkbox('1', "Class 1", ["A", "B", "C", "D", "E","F"]),
                inquirer.Checkbox('2', "Class 2", ["A", "B", "C", "D", "E","F"]),
                inquirer.Checkbox('3', "Class 3", ["A", "B", "C", "D", "E","F"]),
                inquirer.Checkbox('4', "Class 4", ["A", "B", "C", "D", "E","F"]),
                inquirer.Checkbox('5', "Class 5", ["A", "B", "C", "D", "E","F"]),
                inquirer.Checkbox('6', "Class 6", ["A", "B", "C", "D", "E","F"]),
                inquirer.Checkbox('7', "Class 7", ["A", "B", "C", "D", "E","F"]),
                inquirer.Checkbox('8', "Class 8", ["A", "B", "C", "D", "E","F"]),
                inquirer.Checkbox('9', "Class 9", ["A", "B", "C", "D", "E","F"]),
                inquirer.Checkbox('10', "Class 10", ["A", "B", "C", "D", "E","F"]),
                inquirer.Checkbox('11', "Class 11", ["A", "B", "C", "D", "E","F"]),
                inquirer.Checkbox('12', "Class 12", ["A", "B", "C", "D", "E","F"])
        ]
        answer = inquirer.prompt(checkboxQuestion)
        print(answer)
        conn.commit()
        function()

def retrieve_attendance_records(parent):
    confirm  = inquirer.list_input("Sure?" ,choices = ["Yes", "Nope"])
    function = globals()[parent]
    if confirm == "Nope":
        function()
    elif confirm == "Yes":
        conn.commit()
        function()

def main():
    questions = [
        inquirer.List(
            "selection", 
            "",
            [
                "Add Student Names",
                "Enter Attendance Records",
                "Retrieve Attendance Records"
            ]
        )    
    ]
    answer = inquirer.prompt(questions=questions)
    choice = answer["selection"].replace(" ", "_").lower()
    function = globals()[choice]
    function("main")

if __name__ == "__main__":
    try:
        typer.run(main)
    except ms.Error as sqlError:
        print("error")
        print(sqlError)
        if isinstance(sqlError, ms.InterfaceError):
            print("Error with the data. Please recheck the database for the upcoming entry.")
            typer.run(main)
    except Exception as e:
        typer.run(main)