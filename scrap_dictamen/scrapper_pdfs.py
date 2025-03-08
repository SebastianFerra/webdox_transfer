
import os
import shutil

def get_dictamen_name(name):

    start = 0 
    for k in range(len(name)):
        if name[k].isnumeric() and start == 0:
            start = k
        elif name[k] == " " and start != 0:
            end = k
            break

    return name[start:end]
def extract_dictamen(link):

    start = link.find('_')
    width = len("_")
    i = 0
    while start+width+i < len(link):
        if link[start+width+i]==".":
            end = start+width+i
            break
        i += 1
    return link[start+width: end], [start+width, end]
dwld_path = '/Users/sferra/Downloads'

file_names = os.listdir(dwld_path)
for item in file_names:
    if "dictamen" not in item:
        file_names.remove(item)

with open('data_dictamenes.txt', 'r') as f:
    data = f.readlines()

doc_idx = -2
name_idx = 0
moved =[]
not_moved = []

for line in data:
    pass
    if len(line) < 10:
        continue
    cl = line.split(";")
    name = get_dictamen_name(cl[name_idx])
    if name in moved:
        name = name + " (1)"
    aux = cl[doc_idx]
    for file_name in file_names:
        dict_name, idx = extract_dictamen(file_name)
        if name == dict_name:
            shutil.move(dwld_path+r"/"+file_name , f'scrap_dictamen/pdf_recpt/'+aux+".pdf")
            moved.append(name)
            break

    
