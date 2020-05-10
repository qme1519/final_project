import csv
import re
import random

# csv input handling
def csvInput(uploadedFile):
    # convert uploaded file to csv reader
    try:
        csv_reader = csv.reader(uploadedFile)
    except:
        return "Couldn't load csv file"
    # input data from csv to array
    for row in csv_reader:
        values = row[0].split(";")
    # remove any blank values
    for i in values:
        if i =='':
            values.remove('')
    # remove encoding artefacts
    while not values[0][0].isdigit():
        values[0] = values[0][1:]
    # convert numbers to integers
    for i in range(len(values)):
        try:
            values[i] = int(values[i])
        except:
            return "CSV files contains non-digit characters"
    return values

def cleanUp(txt):
    # find all numbers in the input
    values = re.findall("-?[0-9]+", txt)
    #convert them to integers
    for i in range(len(values)):
        try:
            values[i] = int(values[i])
        except:
            return False
    return values

def randomArray(description):
    random.seed()
    # read in and validate syntax
    syntax = re.findall("-?[0-9]+", description)
    if len(syntax) != 3:
        return False
    try:
        start = int(syntax[0])
        end = int(syntax[1])
        num = int(syntax[2])
    except:
        return "Input syntax contains non-digit characters"
    # validate number of elements

    if num <= 0:
        return "Invalid number of elements (has to be more than 0)"
    values = []
    # create random array
    for i in range(num):
        values.append(random.randrange(start, end))
    return values
