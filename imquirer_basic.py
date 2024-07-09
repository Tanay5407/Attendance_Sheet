import inquirer
from inquirer.themes import GreenPassion
questions_text = [
    inquirer.Text('name', "Whats the name"),
    inquirer.Text('surname', "Whats the surname")
]

questions_options = [
    inquirer.List('size', "What size do you need", ["S1", "S2", "S3"])
]

questions_check_box = [
    inquirer.Checkbox('interests', "What are you interested in", ['Shirt', 'T-Shirt', 'Pants', 'Jeans'])
]

answers1 = inquirer.prompt(questions=questions_text)
answers2 = inquirer.prompt(questions=questions_options)
answers3 = inquirer.prompt(questions=questions_check_box)

print(answers1['name'], answers1['surname'])
print(answers2['size'])
print(answers3['interests'])