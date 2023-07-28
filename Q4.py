# Assignment - Q4

import pandas as pd

class Person:

    def __init__(self):
        self.attributes = {}
    def new_attribute(self, attribute, value) :
        self.attributes[attribute] = value
    def __repr__(self):
        val = [value for value in self.attributes.values()]
        return val

def create_objects(data):

    person = []

    for row_num, row in data.iterrows():
        people = Person()
        for col in data.columns :
            people.new_attribute(col, row[col])
        person.append(people)
    
    return person

# Input data from excel

df = pd.read_excel('Q4-input.xlsx')

attribute_list = df.columns.tolist()
data_list = df.values.tolist()

data = pd.DataFrame(data_list, columns = attribute_list)

output = create_objects(data)

# Printing output

persondetails = []

for i, val in enumerate(output):
    persondetails.append(val.__repr__())

print('\n',pd.DataFrame(persondetails, index = [f'Person {p+1}' for p in range(len(persondetails))], columns = attribute_list),'\n')

# User input
print('User generated input - type 0 anytime to terminate')

while True:
    
    person_number = int(input('Enter person number -\n'))
    if person_number == 0:
        break
    elif person_number not in range(1,len(persondetails)+1):
        print('Invalid\n')
        continue
    
    attribute_chosen = input(f'Enter attribute (from {attribute_list}) -\n')
    if attribute_chosen == 0:
        break
    elif attribute_chosen not in attribute_list:
        print('Invalid\n')
        continue
    
    if person_number in range(1,len(persondetails)+1) and attribute_chosen in attribute_list:
        print(output[person_number-1].attributes[attribute_chosen],'\n')
    else:
        print('Invalid\n')
        continue