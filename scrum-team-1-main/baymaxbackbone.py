from genericpath import exists
from pytest import skip
from sqlalchemy import false, true
import os
import configparser
from tkinter import *
import xml.etree.ElementTree as ET
import integrateAnnotations
import bioCConverter
import indexer
from elasticsearch import Elasticsearch
from subprocess import call

def navigator(pathToInput, pathToWorkbench, pathToWorkbench2,readyToIndex, readyToIntegrate):
    Directories = os.listdir(pathToInput)
    for object in Directories:
        if(object == 'workbench' or object == 'workbench2' or object == 'workbench3' or object == 'workbench4'): continue  
        if(os.path.isfile(pathToInput + object)):
            if(readyToIndex): 
                indexer.indexer(pathToInput, index, 0)
                break
            elif(readyToIntegrate): integrateAnnotations.integrate(pathToInput + "/", pathToWorkbench, pathToWorkbench2)
            else: bioCConverter.converter(pathToInput, pathToWorkbench)
        else:
            navigator(pathToInput + object +"/" , pathToWorkbench, pathToWorkbench2,readyToIndex, readyToIntegrate)

def makeDirectory(pathToInput,name):
    os.chdir(pathToInput)
    if not os.path.exists(name):
        os.mkdir(name)
    return pathToInput + name + "/" 

def removeDirectory(pathToInput, pathToWorkbench, name):
    Files = os.listdir(pathToWorkbench)
    if(len(Files) != 0):
        for xml in Files:
            os.remove(pathToWorkbench + xml)
    os.chdir(pathToInput)
    os.rmdir(name)

def main():
    if(os.path.isfile(pathToInput)):
        print("The input path leads straight to a XML-FIle. Please reference a directory containing those files. Press enter to exit the programm.")
        input()
        exit()
        
        
    if(task == str(1)):
        print('please launch elasticsearch and kibana now. Once Both loaded continue with any key')
        input()
        navigator(pathToInput, "", "", True, False)

    elif(task == str(2)):        
        pathToWorkbench = makeDirectory(pathToInput, "workbench")    
        navigator(pathToInput, pathToWorkbench, "", False, False) #toBiocC
        pathToWorkbench2 = makeDirectory(pathToInput, "workbench2")            
        pathToWorkbench3 = makeDirectory(pathToInput, "workbench3")       
        os.chdir(pathToRessources+"/GNormPlusJava")        
        os.system('java -Xmx10G -Xms10G -jar GNormPlus.jar ' + pathToWorkbench + ' ' + pathToWorkbench2 +' setup.txt')
        removeDirectory(pathToInput,pathToWorkbench, "workbench")
        #integrateAnnotations.integrate(pathToInput, pathToWorkbench2, pathToWorkbench3)
        navigator(pathToInput, pathToWorkbench2, pathToWorkbench3, False, True)  #integrate
        print('please launch elasticsearch and kibana now. Once Both loaded continue with any key')
        input()          
        indexer.indexer(pathToWorkbench3, index, 0)  #index
        removeDirectory(pathToInput,pathToWorkbench2, "workbench2")
        removeDirectory(pathToInput,pathToWorkbench3, "workbench3")

    elif(task == str(3)):                
        pathToWorkbench = makeDirectory(pathToInput, "workbench")    
        pathToWorkbench2 = makeDirectory(pathToInput, "workbench2")           
        pathToWorkbench3 = makeDirectory(pathToInput, "workbench3")    
        navigator(pathToInput, pathToWorkbench, "",False, False) #toBiocC      
        os.chdir(pathToRessources+"/DNorm-0.0.7")      
        os.system('./RunDNorm_BioC.sh config/banner_NCBIDisease_TEST.xml data/CTD_diseases.tsv output/simmatrix_NCBIDisease_e4.bin '+ pathToWorkbench + ' ' + pathToWorkbench2)
        removeDirectory(pathToInput,pathToWorkbench, "workbench")
        navigator(pathToInput, pathToWorkbench2, pathToWorkbench3, False, True)  #integrate
        print('please launch elasticsearch and kibana now. Once Both loaded continue with any key')
        input()          
        indexer.indexer(pathToWorkbench3, index, 0)  #index
        removeDirectory(pathToInput,pathToWorkbench2, "workbench2")
        removeDirectory(pathToInput,pathToWorkbench3, "workbench3")
        
    elif(task == str(4)):            
        pathToWorkbench = makeDirectory(pathToInput, "workbench")    
        pathToWorkbench2 = makeDirectory(pathToInput, "workbench2")           
        pathToWorkbench3 = makeDirectory(pathToInput, "workbench3")
        pathToWorkbench4 = makeDirectory(pathToInput, "workbench4")
        navigator(pathToInput, pathToWorkbench,"" ,False, False) #toBiocC      
        os.chdir(pathToRessources+"/GNormPlusJava") 
        os.system('java -Xmx10G -Xms10G -jar GNormPlus.jar ' + pathToWorkbench + ' ' + pathToWorkbench2 +' setup.txt')  
        removeDirectory(pathToInput,pathToWorkbench, "workbench")        
        os.chdir(pathToRessources+"/DNorm-0.0.7")      
        os.system('./RunDNorm_BioC.sh config/banner_NCBIDisease_TEST.xml data/CTD_diseases.tsv output/simmatrix_NCBIDisease_e4.bin '+ pathToWorkbench2 + ' ' + pathToWorkbench3)
        removeDirectory(pathToInput,pathToWorkbench2, "workbench2")
        navigator(pathToInput, pathToWorkbench3, pathToWorkbench4, False, True)  #integrate          
        print('please launch elasticsearch and kibana now. Once Both loaded continue with any key')
        input()
        indexer.indexer(pathToWorkbench4, index, 0)  #index
        removeDirectory(pathToInput,pathToWorkbench3, "workbench3")
        removeDirectory(pathToInput,pathToWorkbench4, "workbench4")

    else :
        print('please launch elasticsearch and kibana now. Once Both loaded continue with any key')
        input()
     
    path_to_python=configfile['Start']['path_to_python']
    os.chdir(pathToRessources+ "scrum-team-1/")
    call([path_to_python, "Webapp/server.py"])
    input()
    
es = Elasticsearch()
configfile = configparser.ConfigParser()
configfile.read('config.ini')
print("Welcome to Baymax Back Bone! \r\nHow can I help? Search on Certain Index-0, Index new Studies-1, Annotate Genes-2, Annotate Disease-3, Annotate Genes+Diseases-4")
task = input()
print("Alright! Finally please enter the index")
index = input()
index = index.lower()
pathToInput = configfile['Start']['path_to_originals']
pathToRessources = configfile['Start']['path_to_resources']
os.chdir(pathToRessources+ "scrum-team-1/")        
configfile.set('Start','index',index)
with open('config.ini', 'w') as updatedIniFile:
    configfile.write(updatedIniFile)
main()
