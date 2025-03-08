
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from time import sleep 
import time
import pickle as pkl
import ast
from selenium.webdriver.chrome.service import Service
import os
import random
# set the path of the webdriver
chrome_options = webdriver.ChromeOptions()
dwld_path = "/Users/sferra/Desktop/Pruebas/scrap_circulares/pdf_first"
final_path = "/Users/sferra/Desktop/Pruebas/scrap_circulares/pdf_recpt"
prefs = {
    "download.default_directory": dwld_path,  # Change this to your desired download path
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # Ensure PDFs are downloaded instead of opened
}
chrome_options.add_experimental_option("prefs", prefs)

# Initialize the WebDriver
service = Service('/Users/sferra/Desktop/chromedriver-mac-x64/chromedriver')  # Path to your ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

def fix_pdf_name(tex,date, opt =""):
    aux = tex.split(".")
    return aux[0]+opt+"_"+date+"."+aux[1]

has_links = [1,4,5,6,9,11,13,15]
# open file with all info of the circulars
main_doc_idx = 1
descarga_idx = 4
complemento_idx = 5
resolucion_idx = 6
modifica_idx = 9
modificada_por_idx = 11
deroga_idx = 13
derogado_por_idx = 15
def get_file_name(path):
    for file in os.listdir(path):
        if ".pdf" in file:
            return file
        
def wait_for_download_complete(download_folder, timeout=60):
    """Wait for the download to complete by checking the folder."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        files = os.listdir(download_folder)
        if any(".pdf" in file and ".crdownload" not in file for file in files):
            return True
        time.sleep(1)
     
    print("Not downloaded")
    return False
if "covered.pkl" in os.listdir():
    covered = pkl.load(open("covered.pkl", "rb"))
else:
    covered = []
doc_names = []
doc_missing = []

already_downloaded = os.listdir(final_path)
data = pkl.load(open("data_circulares.pkl", "rb"))
for i, row in enumerate(data):

    if len(row) == 0:
        continue

    fecha = row[2]
    number = row[1][0]
    for j, d in enumerate(row):
        if j in has_links and d != "":
            
            if j == main_doc_idx:
                # downloads, waits for download to complete and renames the file
                # this downloads the first file with the main info
                if "javascript" in d[1]:
                    doc_missing.append(row)
                    continue
                print(d)
                if fix_pdf_name(d[2], fecha) in already_downloaded:
                    print("Already downloaded")
                    continue
                driver.get(d[1])
                if wait_for_download_complete(dwld_path):
                    if final_path+"/"+fix_pdf_name(d[2], fecha) in doc_names:
                        print("REPEATED")
                        input()
                        print(row)
                        input()
                    os.rename(dwld_path+"/"+get_file_name(dwld_path), final_path+"/"+fix_pdf_name(d[2], fecha))
                    
            elif j == descarga_idx:
                # downloads, waits for download to complete and renames the file
                print(d)
                if fix_pdf_name(d[2], fecha, "_"+number) in already_downloaded:
                    print("Already downloaded")
                    continue
                driver.get(d[1])
                if wait_for_download_complete(dwld_path):
                    if final_path+"/"+fix_pdf_name(d[2],fecha, opt = "_"+number) in doc_names:
                        print("REPEATED")
                        input()
                        print(row)
                        input()
                    os.rename(dwld_path+"/"+get_file_name(dwld_path), final_path+"/"+fix_pdf_name(d[2],fecha, opt = "_"+number))
            elif j == complemento_idx:
                # downloads, waits for download to complete and renames the file

                # its always a dict 
                if isinstance(d, dict):
                    for l in d.keys():
                        for item in d[l]:
                            
                            if len(item[0]) >1:
                                if "cap" in item[0]:
                                    #dont download this file
                                    continue
                                print(item)
                                if item[2] in already_downloaded:
                                    print("Already downloaded")
                                    continue
                                driver.get(item[1])
                                if wait_for_download_complete(dwld_path):
                                    if final_path+"/"+item[2] in doc_names:
                                        print("REPEATED")
                                        input()
                                        print(row)
                                        input()
                                    os.rename(dwld_path+"/"+get_file_name(dwld_path), final_path+"/"+item[2])
                else:
                    print(d)
                    if fix_pdf_name(d[2], fecha) in already_downloaded:
                        print("Already downloaded")
                        continue
                    driver.get(d[1])
                    if wait_for_download_complete(dwld_path):
                        if final_path+"/"+fix_pdf_name(d[2], fecha) in doc_names:
                            print("REPEATED")
                            input()
                            print(row)
                            input()
                        os.rename(dwld_path+"/"+get_file_name(dwld_path), final_path+"/"+fix_pdf_name(d[2],fecha))
            elif j == resolucion_idx:
                # downloads, waits for download to complete and renames the file
                # its never list of lists, needs name fixing
                print(d)
                if fix_pdf_name(d[2], fecha) in already_downloaded:
                    print("Already downloaded")
                    continue
                driver.get(d[1])
                if wait_for_download_complete(dwld_path):
                    if final_path+"/"+fix_pdf_name(d[2], fecha) in doc_names:
                        print("REPEATED")
                        input()
                        print(row)
                        input()
                    os.rename(dwld_path+"/"+get_file_name(dwld_path), final_path+"/"+fix_pdf_name(d[2], fecha))
            elif j == modifica_idx:
                # is a dict with "modifica" as key, check for more keys just in case

                if isinstance(d, dict):
                    for l in d.keys():
                        for item in d[l]:
                            if len(item[0]) >1:
                                if "cap" in item[0]:
                                    #dont download this file
                                    continue
                                if item[2] in already_downloaded:
                                    print("Already downloaded")
                                    continue
                                driver.get(item[1])
                                if wait_for_download_complete(dwld_path):
                                    if final_path+"/"+item[2] in doc_names:
                                        print("REPEATED")
                                        input()
                                        print(row)
                                        input()
                                    os.rename(dwld_path+"/"+get_file_name(dwld_path), final_path+"/"+item[2])
                else:
                    print(d)
                    if fix_pdf_name(d[2], fecha) in already_downloaded:
                        print("Already downloaded")
                        continue
                    driver.get(d[1])
                    if wait_for_download_complete(dwld_path):
                        if final_path+"/"+fix_pdf_name(d[2], fecha) in doc_names:
                            print("REPEATED")
                            input()
                            print(row)
                            input()
                        os.rename(dwld_path+"/"+get_file_name(dwld_path), final_path+"/"+fix_pdf_name(d[2],fecha))
            elif j == modificada_por_idx:
                # is a dict with "modificada_por" as key, check for more keys just in case
                if isinstance(d, dict):
                    for l in d.keys():
                        for item in d[l]:
                            if len(item[0]) >1:
                                if "cap" in item[0]:
                                    #dont download this file
                                    continue
                            
                                print(item)
                                if item[2] in already_downloaded:
                                    print("Already downloaded")
                                    continue
                                driver.get(item[1])
                                if wait_for_download_complete(dwld_path):
                                    if final_path+"/"+item[2] in doc_names:
                                        print("REPEATED")
                                        input()
                                        print(row)
                                        input()
                                    os.rename(dwld_path+"/"+get_file_name(dwld_path), final_path+"/"+item[2])
                else:
                    print(d)
                    if fix_pdf_name(d[2], fecha) in already_downloaded:
                        print("Already downloaded")
                        continue
                    driver.get(d[1])
                    if wait_for_download_complete(dwld_path):
                        if final_path+"/"+fix_pdf_name(d[2], fecha) in doc_names:
                            print("REPEATED")
                            input()
                            print(row)
                            input()
                        os.rename(dwld_path+"/"+get_file_name(dwld_path), final_path+"/"+fix_pdf_name(d[2],fecha))
            elif j == deroga_idx:
                # is a dict with "deroga" as key, check for more keys just in case
                if isinstance(d, dict):
                    for l in d.keys():
                        for item in d[l]:
                            if len(item[0]) >1:
                                if "cap" in item[0]:
                                    #dont download this file
                                    continue
                                print(item)
                                if item[2] in already_downloaded:
                                    print("Already downloaded")
                                    continue
                                driver.get(item[1])
                                if wait_for_download_complete(dwld_path):
                                    if final_path+"/"+item[2] in doc_names:
                                        print("REPEATED")
                                        input()
                                        print(row)
                                        input()
                                    os.rename(dwld_path+"/"+get_file_name(dwld_path), final_path+"/"+item[2])
                else:
                    print(d)
                    if fix_pdf_name(d[2], fecha) in already_downloaded:
                        print("Already downloaded")
                        continue
                    driver.get(d[1])
                    if wait_for_download_complete(dwld_path):
                        if final_path+"/"+fix_pdf_name(d[2], fecha) in doc_names:
                            print("REPEATED")
                            input()
                            print(row)
                            input()
                        os.rename(dwld_path+"/"+get_file_name(dwld_path), final_path+"/"+fix_pdf_name(d[2],fecha))
            elif j == derogado_por_idx:
                # is a dict with "derogado_por" as key, check for more keys just in case
                if isinstance(d, dict):
                    for l in d.keys():
                        for item in d[l]:
                            if len(item[0]) >1:
                                if "cap" in item[0]:
                                    #dont download this file
                                    continue
                                print(item)
                                if item[2] in already_downloaded:
                                    print("Already downloaded")
                                    continue
                                driver.get(item[1])
                                if wait_for_download_complete(dwld_path):
                                    if final_path+"/"+item[2] in doc_names:
                                        print("REPEATED")
                                        input()
                                        print(row)
                                        input()
                                    os.rename(dwld_path+"/"+get_file_name(dwld_path), final_path+"/"+item[2])
                else:
                    print(d)
                    if fix_pdf_name(d[2], fecha) in already_downloaded:
                        print("Already downloaded")
                        continue
                    driver.get(d[1])
                    if wait_for_download_complete(dwld_path):
                        if final_path+"/"+fix_pdf_name(d[2], fecha) in doc_names:
                            print("REPEATED")
                            input()
                            print(row)
                            input()
                        os.rename(dwld_path+"/"+get_file_name(dwld_path), final_path+"/"+fix_pdf_name(d[2],fecha))
    covered.append(i)
    #update the list of files
    pkl.dump(covered, open("covered.pkl", "wb"))

for r in doc_missing:
    print(r)
    