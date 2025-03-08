""" 
From each pdf we need:
    - Name of the file
    - Url of download
    - Raw text of the pdf
    - Section or reason to be 
    - Type of document relating to the circular
For each row in the table we need:
    - Type of circular
    - Date of the circular
    - Number of the circular
    - Titulo/Referencia 
    - Texto_refundido (pdf)
    - InformeNormativo/DocumentosComplementarios (pdf many)
    - Resolucion (pdf/date/reference)
    - Modifica a (pdf/date)
    - Modificada por (pdf/date)
    - Deroga a (pdf/date many)
    - Derogada por (pdf/date many)
    - Vigencia (Usually None)
Example JSON:
{
    "circular": {
        "name": "circular_1_2021.pdf",
        "url": "https://www.cmfchile.cl/institucional/mercado-de-valores/circulares/circular_1_2021.pdf",
        "title": "Texto de la circular",
        "date": "01/01/2001",
        "type": "NCG"
        "refundido": {
            "name": "refundido_1_2021.pdf",
            "url": "https://www.cmfchile.cl/institucional/mercado-de-valores/circulares/refundido_1_2021.pdf",
            "title": "Texto refundido"
                    },
        "complement": {
            "0":{
            "name": "complement_1_2021.pdf",
            "url": "https://www.cmfchile.cl/institucional/mercado-de-valores/circulares/complement_1_2021.pdf",
            "title": "Informe normativo"
            "text": "Texto del informe normativo"
                    },
            "1":{
            "name": "complement_1_2021.pdf",
            "url": "https://www.cmfchile.cl/institucional/mercado-de-valores/circulares/complement_1_2021.pdf",
            "title": "Complemento"
            "text": "Texto del complemento"
                    }
                        },
        "resolution": {

            "name": "resolution_1_2021.pdf",
            "url": "https://www.cmfchile.cl/institucional/mercado-de-valores/circulares/resolution_1_2021.pdf",
            "title": "Resolucion",
            "date": "01/01/2001",
            "reference": "Resolucion 1"
            "text": "Texto de la resolucion"
                    },
        "modify": {
            "0":{
            "number": "1",
            "name": "modify_1_2021.pdf",
            "url": "https://www.cmfchile.cl/institucional/mercado-de-valores/circulares/modify_1_2021.pdf",
            "title": "Modifica a"
            "date": "01/01/2001"
            "text": "Texto de la modificacion"
                    },
            "1":{
            "number": "2",
            "name": "modify_2_2021.pdf",
            "url": "https://www.cmfchile.cl/institucional/mercado-de-valores/circulares/modify_2_2021.pdf",
            "title": "Modifica a"
            "date": "01/01/2001"
            "text": "Texto de la modificacion"
                    }
                        },
        "modified": {
            "0":{
            "number": "1",
            "name": "modified_1_2021.pdf",
            "url": "https://www.cmfchile.cl/institucional/mercado-de-valores/circulares/modified_1_2021.pdf",
            "title": "Modificada por"
            "date": "01/01/2001"
            "text": "Texto de la modificacion"
                    },
            "1":{
            "number": "2",
            "name": "modified_2_2021.pdf",
            "url": "https://www.cmfchile.cl/institucional/mercado-de-valores/circulares/modified_2_2021.pdf",
            "title": "Modificada por"
            "date": "01/01/2001"
            "text": "Texto de la modificacion"
                    }
                        },
        "derogate": {
            "0":{
            "number": "1",
            "name": "derogate_1_2021.pdf",
            "url": "https://www.cmfchile.cl/institucional/mercado-de-valores/circulares/derogate_1_2021.pdf",
            "title": "Deroga a"
            "date": "01/01/2001"
            "text": "Texto de la derogacion"
                    },
            "1":{
            "number": "2",
            "name": "derogate_2_2021.pdf",
            "url": "https://www.cmfchile.cl/institucional/mercado-de-valores/circulares/derogate_2_2021.pdf",
            "title": "Deroga a"
            "date": "01/01/2001"
            "text": "Texto de la derogacion"
                    }
                        },
        "derogated": {
            "0":{
            "number": "1",
            "name": "derogated_1_2021.pdf",
            "url": "https://www.cmfchile.cl/institucional/mercado-de-valores/circulares/derogated_1_2021.pdf",
            "title": "Derogada por"
            "date": "01/01/2001"
            "text": "Texto de la derogacion"
                    },
            "1":{
            "number": "2",
            "name": "derogated_2_2021.pdf",
            "url": "https://www.cmfchile.cl/institucional/mercado-de-valores/circulares/derogated_2_2021.pdf",
            "title": "Derogada por"
            "date": "01/01/2001"
            "text": "Texto de la derogacion"
                    }
                        },
        "vigency": None
    }
"""



# imports
import pickle as pkl
import os
import pypdf
import json
############
# imports for OCR
from paddleocr import PaddleOCR, draw_ocr
import pytesseract
import paddle
import pandas as pd
import os
import sys

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

def download_and_load_models():
    """Need to run only once to download and load model into memory.
    English model works better than Spanish in most cases."""
    try:
        ocr = PaddleOCR(use_angle_cls=True, lang='en',use_gpu=False, show_log = False) # ,show_log = False
        print("Model loaded successfully")
        font_path = os.path.join('PaddleOCR', 'doc', 'fonts', 'latin.ttf')
        print("Fonth path  successfully")
        return ocr
        
    except Exception as e:
        print(f"An error occurred while loading the model: {e}", file=sys.stderr)

ocr = download_and_load_models()

def detect_entities_in_image(ocr,img_path):
    result = ocr.ocr(img_path, cls=True)
    entities_ocr_output = []
    ocr_output = []
    for idx in range(len(result)):
        res = result[idx]
        if res is not None:
            for line in res:
                ocr_output.append(line)
                entities_ocr_output.append(line[1])
    contract = ""
    for text,confidence in entities_ocr_output:
        if confidence > 0.8:
            contract += text + "\n"
    return contract

gpu_available  = paddle.device.is_compiled_with_cuda()
print("GPU available:", gpu_available)
#######

# functions
def date_to_str(date):
    aux = date.split("/")
    return aux[0]+"_"+aux[1]+"_"+aux[2]
def fix_pdf_name(tex,date, opt =""):
    aux = tex.split(".")
    return aux[0]+opt+"_"+date+"."+aux[1]
def manage_pdf(pdf_path):
    pdf = pypdf.PdfReader(open(pdf_path, "rb"))
    text = pdf.pages[0].extract_text()
    if text == "":
        print(f"Old pdf, need managing: {pdf_path}")
        print("Applying OCR")
        raw_text = detect_entities_in_image(ocr,pdf_path)
        title = pdf_path.split(".")[0]
        return title, raw_text
    first_jump = text.find("\n")
    title = text[:first_jump]
    text = text[first_jump:]
    return title, text


# get the data from the pkl file
data = pkl.load(open("data_circulares.pkl", "rb"))
# create the json file

if not os.path.exists("circulares.json"):
    json_data = {}
else:
    with open("circulares.json", "r") as f:
        json_data = json.load(f)


# path to get the pdfs
path_pdfs = "pdf_recpt/" 

# useful indexes for naming
main_doc_idx = 1
descarga_idx = 4
complemento_idx = 5
resolucion_idx = 6
modifica_idx = 9
modificada_por_idx = 11
deroga_idx = 13
derogado_por_idx = 15




# iterate over the data
for row in data:
    
    if len(row) == 0:
        continue

    json_name = row[0]+"_"+row[1][0]
    
    if json_name in json_data.keys():
        continue
    
    print(json_name)
    # update circulares.txt
    with open("data_circulares.txt", "a") as f:
        for i in range(len(row)):
            f.write(str(row[i]))
            f.write(";")
        f.write("\n")

    # create the json for the circular
    circular = {}
    circular["name"] = fix_pdf_name(row[1][-1],row[2])
    circular["url"] = row[1][1]
    circular["title"], circular["text"]= manage_pdf(path_pdfs+circular["name"])
    circular["date"] = row[2]
    circular["type"] = row[0]
    
    # create the json for the refundido
    if row[descarga_idx] != "":
        refundido = {}
        refundido["name"] = fix_pdf_name(row[descarga_idx][-1],row[2], "_"+row[1][0])
        refundido["url"] = row[descarga_idx][1]
        refundido["title"], refundido["text"] = manage_pdf(path_pdfs+refundido["name"])
        circular["refundido"] = refundido
    else:
        circular["refundido"] = None
    
    # create the json for the complement
    complement = {}
    if row[complemento_idx] != "":
        if isinstance(row[complemento_idx], dict):
            # many complementos
            for i, l in enumerate(row[complemento_idx].keys()):
                for item in row[complemento_idx][l]:
                    if item[0] == "":
                        continue
                    complement[i] = {}
                    complement[i]["name"] = item[-1]
                    complement[i]["url"] = item[1]
                    if "cap" in item[0].lower():
                        if "2" in item[0]:
                            complement[i]["title"], complement[i]["text"] = manage_pdf(path_pdfs+"cap2-2.pdf")
                        elif "8" in item[0]:
                            complement[i]["title"], complement[i]["text"] = manage_pdf(path_pdfs+"cap8-1.pdf")
                    else:      
                        complement[i]["title"], complement[i]["text"] = manage_pdf(path_pdfs+complement[i]["name"])
        else:
            complement[0] = {}
            complement[0]["name"] = fix_pdf_name(row[complemento_idx][-1], row[2])
            complement[0]["url"] = row[complemento_idx][1]
            complement[0]["title"], complement[0]["text"] = manage_pdf(path_pdfs+complement[0]["name"])       
    else:
        complement = None
    circular["complement"] = complement
    # create the json for the resolution
    resolution = {}
    if row[resolucion_idx] != "":
        resolution["name"] = fix_pdf_name(row[resolucion_idx][-1], row[2])
        resolution["url"] = row[resolucion_idx][1]
        resolution["title"], resolution["text"] = manage_pdf(path_pdfs+resolution["name"])
        resolution["date"] = row[resolucion_idx+1]
        resolution["reference"] = row[resolucion_idx+2]
        circular["resolution"] = resolution
    else:
        circular["resolution"] = None
    # create the json for the modify
    modify = {}
    if row[modifica_idx] != "":
        if isinstance(row[modifica_idx], dict):
            row[modifica_idx+1] = row[modifica_idx+1].split(" ")
            for i, l in enumerate(row[modifica_idx].keys()):
                for item in row[modifica_idx][l]:
                    if item[0] == "":
                        continue
                    modify[i] = {}
                    modify[i]["number"] = item[0]
                    modify[i]["name"] = item[-1]
                    modify[i]["url"] = item[1]
                    modify[i]["date"] = date_to_str(row[modifica_idx+1].pop(0))
                    modify[i]["title"], modify[i]["text"] = manage_pdf(path_pdfs+modify[i]["name"])

        else:
            modify[0] = {}
            modify[0]["number"] = row[modifica_idx+1]
            modify[0]["name"] = fix_pdf_name(row[modifica_idx][-1], row[2])
            modify[0]["url"] = row[modifica_idx][1]
            modify[0]["date"] = date_to_str(row[modifica_idx+1])
            modify[0]["title"], modify[0]["text"] = manage_pdf(path_pdfs+modify[0]["name"])
    else:
        modify = None
    circular["modify"] = modify

    # create the json for the modified
    modified = {}
    if row[modificada_por_idx] != "":
        if isinstance(row[modificada_por_idx], dict):
            row[modificada_por_idx+1] = row[modificada_por_idx+1].split(" ")
            # many modified
            for i, l in enumerate(row[modificada_por_idx].keys()):
                for item in row[modificada_por_idx][l]:
                    if item[0] == "":
                        continue
                    modified[i] = {}
                    modified[i]["number"] = item[0]
                    modified[i]["name"] = item[-1]
                    modified[i]["url"] = item[1]
                    modified[i]["date"] = date_to_str(row[modificada_por_idx+1].pop(0))
                    modified[i]["title"], modified[i]["text"] = manage_pdf(path_pdfs+modified[i]["name"])
        else:
            modified[0] = {}
            modified[0]["number"] = row[modificada_por_idx+1]
            modified[0]["name"] = fix_pdf_name(row[modificada_por_idx][-1], row[2])
            modified[0]["url"] = row[modificada_por_idx][1]
            modified[0]["date"] = date_to_str(row[modificada_por_idx+1])
            modified[0]["title"], modified[0]["text"] = manage_pdf(path_pdfs+modified[0]["name"])
    else:
        modified = None
    circular["modified"] = modified

    # create the json for the derogate
    derogate = {}
    if row[deroga_idx] != "":
        if isinstance(row[deroga_idx], dict):
            row[deroga_idx+1] = row[deroga_idx+1].split(" ")
            # many derogate
            for i, l in enumerate(row[deroga_idx].keys()):
                for item in row[deroga_idx][l]:
                    if item[0] == "":
                        continue
                    derogate[i] = {}
                    derogate[i]["number"] = item[0]
                    derogate[i]["name"] = item[-1]
                    derogate[i]["url"] = item[1]
                    derogate[i]["date"] = date_to_str(row[deroga_idx+1].pop(0))
                    derogate[i]["title"], derogate[i]["text"] = manage_pdf(path_pdfs+derogate[i]["name"])
        else:
            derogate[0] = {}
            derogate[0]["number"] = row[deroga_idx+1]
            derogate[0]["name"] = fix_pdf_name(row[deroga_idx][-1], row[2])
            derogate[0]["url"] = row[deroga_idx][1]
            derogate[0]["date"] = date_to_str(row[deroga_idx+1])
            derogate[0]["title"], derogate[0]["text"] = manage_pdf(path_pdfs+derogate[0]["name"])
    else:
        derogate = None
    circular["derogate"] = derogate

    # create the json for the derogated
    derogated = {}
    if row[derogado_por_idx] != "":
        if isinstance(row[derogado_por_idx], dict):
            row[derogado_por_idx+1] = row[derogado_por_idx+1].split(" ")
            # many derogated
            for i, l in enumerate(row[derogado_por_idx].keys()):
                for item in row[derogado_por_idx][l]:
                    if item[0] == "":
                        continue
                    derogated[i] = {}
                    derogated[i]["number"] = item[0]
                    derogated[i]["name"] = item[-1]
                    derogated[i]["url"] = item[1]
                    derogated[i]["date"] = date_to_str(row[derogado_por_idx+1].pop(0))
                    derogated[i]["title"], derogated[i]["text"] = manage_pdf(path_pdfs+derogated[i]["name"])
        else:
            derogated[0] = {}
            derogated[0]["number"] = row[derogado_por_idx+1]
            derogated[0]["name"] = fix_pdf_name(row[derogado_por_idx][-1], row[2])
            derogated[0]["url"] = row[derogado_por_idx][1]
            derogated[0]["date"] = date_to_str(row[derogado_por_idx+1])
            derogated[0]["title"], derogated[0]["text"] = manage_pdf(path_pdfs+derogated[0]["name"])
    else:
        derogated = None
    circular["derogated"] = derogated

    # create the json for the vigency
    vigency = {}
    vigency["info"] = row[-1]
    circular["vigency"] = vigency
    json_name = row[0]+"_"+row[1][0]
    if json_name in json_data.keys():
        print("Repeated circular???")
    else:
        json_data[json_name] = circular
    with open("circulares.json", "w") as f:
        json.dump(json_data, f, indent=4)
# save the json file

