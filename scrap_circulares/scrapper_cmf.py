
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from time import sleep 
import os
import ast
import pickle as pkl
import fileinput
# set the path of the webdriver
web_url = 'https://www.cmfchile.cl/institucional/legislacion_normativa/normativa2.php?tiponorma=ALL&numero=&dd=&mm=&aa=&dd2=&mm2=&aa2=&buscar=&entidad_web=ALL&materia=ALL&enviado=1&hidden_mercado=%25&tpl=alt'
driver = webdriver.Chrome() # create a new instance of the Chrome driver
driver.get(web_url) # navigate to the page
sleep(5) # wait for the web page to load
def progress_bar(current, total, barLength = 20):
    progress = current/total
    arrow = "="*int(progress*barLength)
    spaces = " "*int((1-progress)*barLength)
    print(f"\rProgress: [{arrow}{spaces}] {current}/{total}", end = "")
    if current == total:
        print()
# If not first scrap test, delete the previous data
def date_to_str(date):
    if "." in date:
        date = date.split(".")
    elif "/" in date:
        date = date.split("/")
    return date[2]+"_"+date[1]+"_"+date[0]

def fix_pdf_name(tex,date, opt =""):
    aux = tex.split(".")
    return aux[0]+opt+"_"+date+"."+aux[1]

head = ["Tipo de Norma", "Número", "Fecha", "Titulo/Referencia", "Texto refundido/ Hojas de reemplazo", "Informe normativo/ Docs complementarios", "Resolucion numero",
        "Resolucion fecha", "Resolucion referencia", "Modifica a numero", "Modifica a fecha", "Modificada por numero", "Modificada por fecha","Deroga a numero",
        "Deroga a fecha", "Derogada por numero", "Derogada por fecha", "Vigencia"]
# useful indexes for naming
idx_fecha = 2
idx_nro = 1
idx_tipo = 0
idx_res_nro = 6
idx_res_fecha = 7
idx_modifica_nro = 9
idx_modifica_fecha = 10
idx_modificada_nro = 11
idx_modificada_fecha = 12
idx_deroga_nro = 13
idx_deroga_fecha = 14
idx_derogada_nro = 15
idx_derogada_fecha = 16

has_links = [1,4,5,6,9,11,13,15]
links_names = {1:"Nro_norma", 4:"Texto_Refundido", 5:"Complemento", 6:"Resolucion", 9:"Modifica", 11:"Modificada_por", 13:"Deroga", 15:"Derogada_por"}
table = driver.find_elements(By.CLASS_NAME, 'table-responsive') # find the table from where we want to extract the data
# create txt file to save the data

data = []
for i,item in enumerate(table): # all tables in the page
    if i ==0: # skip the first table
        continue
    row = item.find_elements(By.TAG_NAME, 'tr') # rows of the table
    for j, r in enumerate(row):
        list_row =[]
        
        col = r.find_elements(By.TAG_NAME, 'td') # item in rows
        for k, c in enumerate(zip(col,head)):# every item in row
            links_dict = {}
            col_name = head[k]
            # some items are numerous links, we need to extract all of them
            if k not in has_links and k != 2:
                # delete line breaks
                list_row.append(c[0].text.replace("\n", " "))
            elif k == 2:
                date_fixed = date_to_str(c[0].text)
                list_row.append(date_fixed)
                # setup name for files
                file_name_id = list_row[0]+"_"+list_row[1][0]+"_"+date_fixed

            else:
                sub_rows = c[0].find_elements(By.TAG_NAME, 'a')
                lar = 0
                if len(sub_rows) > 1:
                    links_dict = {links_names[k]:[]}
                    lar = 1
                for l, link in enumerate(sub_rows):
                    link_url = link.get_attribute('href')
                    link_name = link.text
                    if lar == 1:
                        file_name = file_name_id + "_" + links_names[k] + "_" + str(l) + ".pdf"
                        links_dict[links_names[k]].append([link_name, link_url, file_name])
                    else:
                        file_name = list_row[0]+"_"+link_name+".pdf"
                        links_dict = [link_name, link_url, file_name]
                
                if bool(links_dict):                  
                    list_row.append(links_dict)
                else:
                    list_row.append("")
            
        
        # fix download item pdf name 
        if len(list_row)>1:
            number = list_row[1][0]
            date = list_row[2]
            if list_row[4] != "":
                list_row[4][2] = fix_pdf_name(list_row[4][2], date, "_"+number)
        #progress bar
        progress_bar(j+1, len(row))
        data.append(list_row)
pkl.dump(data, open("data_circulares.pkl", "wb"))

  


            

