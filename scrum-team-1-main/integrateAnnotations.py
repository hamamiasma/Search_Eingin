import xml.etree.ElementTree as ET
import os
import configparser

#commentar
def integrate(studyOriginals,nlpOutouts,pathToIntegratedStudies):

    studyFiles = os.listdir(studyOriginals)
    #nlpOutputFiles=os.listdir(nlpOutouts)
    for studyFile in studyFiles:
        print("integrate Annotations for: " + studyFile)
        if not studyFile.endswith(".xml"):
            continue
        try:
            studyTree = ET.parse(studyOriginals + studyFile)
            studyRoot = studyTree.getroot()
            #studyTagsElement=ET.SubElement(studyRoot,'biomedical tags')
            annotateTree = ET.parse(nlpOutouts + studyFile)
            annotateRoot = annotateTree.getroot()
        except:
            print("problem with study: "+studyFile)
            continue
        for passage in annotateRoot.iter('passage'):
            passageType = passage.find(".//infon[@key='type']").text
            studyTypeElement = studyRoot.find('.//' + passageType)
            
            ProcessAnnotations(studyRoot, passage, studyTypeElement)
            #ncbi = annotation.find('infon').text
            #annotateSet.add(ncbi)
            #print(ncbi)
            #for annotation in annotateSet:
            #    i = ET.SubElement(studyTypeElement, 'ncbi_tag')
            #    i.text = annotation
        studyTree.write(pathToIntegratedStudies + studyFile)
        #studyTree.write(pathToIntegratedStudies)

def ProcessAnnotations(studyRoot, passage, studyTypeElement):
    DiseaseSet=set()
    GeneSet=set()
    SpeciesSet=set()
    for annotation in passage.iter('annotation'):
        annotationType=annotation.find("infon[@key='type']").text
        classifyAnnotation(annotationType,studyTypeElement, studyRoot, annotation)
        #for existingAnnotationsCount in study

def classifyAnnotation(annotationType,studyTypeElement, studyRoot, annotation):
    #studyTypeElement.append(annotation)
    annotationTag=annotation.find("infon").text
    annotationName=annotation.find("text").text
    studyTagElement=studyRoot.find(".//occuring-" + annotationType)
    studyCountElement=studyRoot.find(".//occuringCounts-" + annotationType)
    if studyTagElement == None:
        studyTagElement=ET.SubElement(studyRoot,"occuring-"+ annotationType)
        studyCountElement=ET.SubElement(studyRoot,"occuringCounts-"+ annotationType)

    found = False
    for existingAnnotationsCount in studyCountElement.iter(annotationType):
        if annotationTag==existingAnnotationsCount.find("standarizedtag").text:
            existingAnnotationsCount.find("count").text=str(int(existingAnnotationsCount.find("count").text)+1)
            found=True
            break
    if not found:
        studyCountElement=ET.SubElement(studyCountElement,annotationType)
        nameElement=ET.SubElement(studyCountElement,"name")
        nameElement.text=annotationName
        nameTagElement=ET.SubElement(studyCountElement,"standarizedtag")
        nameTagElement.text=annotationTag
        countElement=ET.SubElement(studyCountElement,"count")
        countElement.text="1"

    studyTagElement.append(annotation)

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    studyOriginals=config['PREPROCESS']['path_to_study_orignals']
    nlpOutouts=config['PREPROCESS']['path_to_nlp_pipeline_outputs']
    pathToIntegratedStudies=config['PREPROCESS']['path_to_integrated_studies']
    integrate(studyOriginals, nlpOutouts, pathToIntegratedStudies)

if __name__ == '__main__' :
    main()