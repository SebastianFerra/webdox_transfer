
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from time import sleep 
import os
import fileinput
import shutil
# set the path of the webdriver
web_url = 'https://www.cmfchile.cl/institucional/inc/dictamenes.php?aa=%23'
driver = webdriver.Chrome() # create a new instance of the Chrome driver
driver.get(web_url) # navigate to the page
sleep(5) # wait for the web page to load

# If not first scrap test, delete the previous data
try:
    os.remove('data_dictamenes.txt')
except:
    pass
def get_file_num(link):
    start = link.find('docto=')
    width = len("docto=")
    i = 0
    while True:
        if link[start+width+i]=="&":
            end = start+width+i
            break
        i += 1

    return link[start+width: end]

def get_dictamen_name(name):

    start = 0 
    for k in range(len(name)):
        if name[k].isnumeric() and start == 0:
            start = k
        elif name[k] == " " and start != 0:
            end = k
            break
    print(name[start:end])
    return name[start:end]



table = driver.find_element(By.CLASS_NAME, 'table-responsive') # find the table from where we want to extract the data
# create txt file to save the data
with open('data_dictamenes.txt', 'a+') as f:
    row = table.find_elements(By.TAG_NAME, 'tr') # rows of the table
    for j, r in enumerate(row):
        col = r.find_elements(By.TAG_NAME, 'td') # item in rows
        for k, c in enumerate(col):

            t = c.text
            if k == 0:
                name = get_dictamen_name(t)
            if "\n" in t:
                t = t.replace('\n', '')
            f.write(t+";")
            try:
                link = c.find_element(By.TAG_NAME, 'a').get_attribute('href')
                aux = get_file_num(link)
                print(link)
                print(aux)
                driver.get(link)
                #get the file name from the folder
                f.write(name+"_"+aux+";")
                f.write(link)
            except:
                print("no link")
        f.write("\n")



driver.quit() # close the browser



