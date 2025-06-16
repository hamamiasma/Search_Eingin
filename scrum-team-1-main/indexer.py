from elasticsearch import Elasticsearch
from pathlib import Path
from collections import OrderedDict
import xmltodict
import os
import configparser
import xml.etree.ElementTree as ET

es = Elasticsearch()

def indexer(pathToWorkbench, index, id):
    Files = os.listdir(pathToWorkbench)
    for xml in Files:
        if(os.path.isfile(pathToWorkbench + xml)):       
            pathToXml = (pathToWorkbench + "/" + xml)
            studyTree = ET.parse(pathToXml)
            studyRoot = studyTree.getroot()
            for subtitle in studyRoot.iter('sub_title'):
                try:
                    del subtitle.attrib['vocab']
                except:
                        pass 
            studyTree.write(pathToXml)
            file_dict = Path(pathToXml)
            input_dict = xmltodict.parse(file_dict.open("r").read())
            study_dict = input_dict["clinical_study"]
            date_fields = [key for key in study_dict.keys() if "date" in key]

            for key, value in study_dict.items():
                if isinstance(study_dict[key], OrderedDict) and key in date_fields:
                    study_dict[key] = study_dict[key]["#text"]
                if isinstance(value, OrderedDict) and len(value) == 1 and "textblock" in value:
                    study_dict[key] = study_dict[key]["textblock"]
                if isinstance(value, OrderedDict) and len(value) == 1 and "text" in value:
                    study_dict[key] = study_dict[key]["text"]    
                if isinstance(value, OrderedDict) and len(value) == 1 and "#text" in value:
                    study_dict[key] = study_dict[key]["#text"]          
                if isinstance(study_dict[key], OrderedDict) and key == "enrollment" in study_dict.keys():
                    study_dict[key] = study_dict[key]["#text"]
            es.index(index = index, id = id, body=study_dict)
        id=id+1
    es.indices.refresh(index)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    pathToStudies=config['PREPROCESS']['path_to_study_orignals']
    index=config['Start']['index']
    indexer(pathToStudies,index,0)
    

if __name__ == '__main__' :
    main()
