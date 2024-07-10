#including libraries
import mysql.connector as ms
import datetime as dt
import inquirer
import typer
import tabulate

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
        
Headers = ["ADMIN", "NAME"]
for i in range(1,13):
    table_name = f"{i}_{year}"
    command = f"CREATE TABLE IF NOT EXISTS {table_name} (Admin VARCHAR(10),"
    if i in [1,3,5,7,8,10,12]:
        for j in range(1,32):
            command = command + f"`{j}` VARCHAR(3) DEFAULT NULL, "
            Headers.append(j)
    if i in [4,6,9,11]:
        for j in range(1,31):
            command = command + f"`{j}` VARCHAR(3) DEFAULT NULL, "
            Headers.append(j)
    if i == 2:
        if leap == True:
            for j in range(1,30):
                command = command + f"`{j}` VARCHAR(3) DEFAULT NULL, "
                Headers.append(j)
        if leap == False:
            for j in range(1,29):
                command = command + f"`{j}` VARCHAR(3) DEFAULT NULL, "
                Headers.append(j)
    command = command[:-2]
    command = command + ");"
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
        for i in range(1,13):
            table_name = f"{i}_{year}"
            insert_query = f"INSERT INTO {table_name}(Admin) values('{Admin}');"
            print(insert_query)
            cursor.execute(insert_query)
        conn.commit()
        function()

def enter_attendance_records(parent):
    """Function to enter student attendance records"""
    confirm  = inquirer.list_input("Sure?" ,choices = ["Yes", "Nope"])
    function = globals()[parent]
    if confirm == "Nope":
        function()
    elif confirm == "Yes":
        Class = typer.prompt("Which Class")
        Section = typer.prompt("Which Section")
        cursor.execute(f"SELECT * FROM names WHERE CLASS = '{Class}' and Section ='{Section}'")
        res = cursor.fetchall()
        data = []
        for i in range(len(res)):
            record = res[i]
            admin = record[0]
            name = record[1]
            data.append([admin, name])
        for i in range(len(data)):
            choice = typer.prompt(f"Present Or Absent ( {data[i][1]} ) ")
            update_query = f"UPDATE {month}_{year} SET `{day}` = '{choice}' WHERE ADMIN = '{data[i][0]}';"
            print(update_query)
            cursor.execute(update_query)
        conn.commit()
        function()
        return res

def retrieve_attendance_records(parent):
    confirm  = inquirer.list_input("Sure?" ,choices = ["Yes", "Nope"])
    function = globals()[parent]
    if confirm == "Nope":
        function()
    elif confirm == "Yes":
        Month = typer.prompt("Which Month")
        Year = typer.prompt("Which Year")
        Class = typer.prompt("Which Class")
        Section = typer.prompt("Which Section")
        retrieve_query = f"SELECT * FROM NAMES WHERE CLASS = '{Class}' AND SECTION = '{Section}';"
        cursor.execute(retrieve_query)
        res = cursor.fetchall()
        data = []
        for i in range(len(res)):
            admin = res[i][0]
            data.append(admin)
        res = []
        for i in range(len(data)):
            retrieve_query = f"SELECT * FROM {Month}_{Year} WHERE ADMIN = '{data[i]}';"
            cursor.execute(retrieve_query)
            res.append(cursor.fetchall()[0])
        print(tabulate.tabulate(res, headers = Headers, tablefmt="rounded_outline"))
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
