import xml.etree.ElementTree as ET
import os
from datetime import date
import configparser


def add_new_document(root, documentId):
    document = ET.SubElement(root, 'document')
    idElement = ET.SubElement(document, 'id')
    idElement.text = documentId
    return document


def add_new_passage(document, passageType, offset, text):
    passage = ET.SubElement(document, 'passage')
    infonElement = ET.SubElement(passage, 'infon')
    infonElement.set('key', 'type')
    infonElement.text = passageType
    offsetElement = ET.SubElement(passage, 'offset')
    offsetElement.text = str(offset)
    textElement = ET.SubElement(passage, 'text')
    textElement.text = text

def add_study(studyRoot, documentElement):
    position = 0
    for element in studyRoot.iter():
        for child in element:
            if child.tag == 'textblock':
                textblock=child.text.replace("\n","")
                textblock=textblock.replace("\r","")
                textblock=textblock.replace(". .",".")
                add_new_passage(documentElement, element.tag, position, textblock)
                position += len(textblock)
                #pubtatorFile.write(element.tag + "|text|" + textblock + "\n\n")
                # print('Der Text: \n' + child.text + '\n ist so lang:' + str(len(child.text)))

#bioCRoot = ET.Element('collection')
def converter(pathToStudies,pathToBioCOutput):
    studyFiles = os.listdir(pathToStudies)
    for studyFile in studyFiles:
        if(os.path.isfile(pathToStudies + "/" + studyFile) and studyFile.endswith(".xml")):
            #print("Converting XML-File to BioC-XML: " + studyFile)
            bioCRoot = ET.Element('collection')
            sourceElement = ET.SubElement(bioCRoot, 'source')
            sourceElement.text = 'https://clinicaltrials.gov'
            dateElement = ET.SubElement(bioCRoot, 'date')
            today = date.today()
            dateElement.text = today.strftime("%B %d, %Y")
            keyElement = ET.SubElement(bioCRoot, 'key')
            keyElement.text = ''
            studyTree = ET.parse(pathToStudies + '/' + studyFile)
            studyRoot = studyTree.getroot()
            studyId = studyRoot.get('rank')
            documentElement = add_new_document(bioCRoot, studyId)
            #pubtatorFile = open(pathToPubTatorOutput + studyFile + ".pubtator","w")
            add_study(studyRoot, documentElement)
            #pubtatorFile.close()
            bioCTree = ET.ElementTree(bioCRoot)
            bioCTree.write(pathToBioCOutput + studyFile)

#xmlTree = ET.parse(path + '/000/00000/NCT00000102.xml')
#firstDocument = add_new_document_to_tree(bioCRoot, '1')
    #add_study(xmlTree, firstDocument)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    pathToStudies=config['PREPROCESS']['path_to_study_orignals']
    pathToBioCOutput=config['PREPROCESS']['path_to_reduced_studies_in_bioc_xml']
    #pathToPubTatorOutput=config['PREPROCESS']['path_to_reduced_studies_in_pubtator_format']

    for root, dirs, files in os.walk(pathToStudies):
        for dir in dirs:
            converter(pathToStudies+dir,pathToBioCOutput)
    

if __name__ == '__main__' :
    main()