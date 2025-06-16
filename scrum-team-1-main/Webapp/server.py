import math
from typing import Dict, List
from tracemalloc import stop
from flask import Flask, render_template, url_for, request
from elasticsearch import Elasticsearch
import configparser



#Setting up the flask app and elasticsearch api connection:
app = Flask(__name__)
es = Elasticsearch( port=9200)

configfile = configparser.ConfigParser()
configfile.read('config.ini')

index = configfile['Start']['index']










def es_body (search_term, disease_id, gene_id , phase_term, status_term, hits_from, RESULTS_PER_PAGE ):
     phase_default = ['N/A', 'Phase 1', 'Phase 2', 'Phase 3', 'Phase 4', 'Early Phase 1', 'Phase 1/Phase 2', 'Phase 2/Phase 3']
     status_default = ['Completed', 'Not yet recruiting', 'Active, not recruiting', 'Terminated', 'Enrolling by invitation', 'Withdrawn', 'Unknown status', 'Recruiting', 'No Longer available', 'Available', 'Withheld']
     
    # if phase_term and status_term are empty lists 
     if not phase_term :

        phase_term = phase_default
     if not status_term :    
        status_term= status_default

    
    
    #1SEarchT   
     if(disease_id == "" and search_term != "" and gene_id =="" ):
          res = es.search(
       
          index= index, #insert index name   

          body={       
              "from":hits_from, 
              "size": RESULTS_PER_PAGE,
              "query": {
                  
                  "bool": {   

                      
                       "must": [
                          

                #must1 searchquery
                {"multi_match" : {
                    
                    "query": search_term, 
                    #and operator interprets our search term as a match_phrase query 
                    "operator" : "and" 
                    } },
            
             

                #must 2 filter phase
                 
                 #term query and keyword fields dont get tokenized in search
                 { "terms": { "phase.keyword": phase_term}},


                #must 3 filter status 
                 
                 #term query and keyword fields dont get tokenized in search
                 { "terms": { "overall_status.keyword": status_term }}
               

                 
                 
                          
                                        ]
              
              
              }
            }
           }
        )
    
    #2DiseaseID
     if(disease_id != "" and search_term == "" and gene_id ==""):
        res = es.search(
        index=index , #insert index name

        body={
            "from":hits_from, 
            "size": RESULTS_PER_PAGE,
            "query": {
                              
                     "multi_match":{ 
                       
                       "query": disease_id,
                       "operator": "or",
                       "fields": "occuring-Disease.annotation.infon.#text"
              
     
            
                                 }
                
            }
        }
    )  
    #3NIchts eingegeben
     if(disease_id == "" and search_term == "" and gene_id ==""):
        res=[]
    #4SearchT und Disease    
     if(disease_id != "" and search_term != "" and gene_id ==""):
             res = es.search(
       
          index= index, #insert index name   

          body={       
              "from":hits_from, 
              "size": RESULTS_PER_PAGE,
              "query": {
                  
                  "bool": {   

                      
                       "must": [
                          

                #must1 searchquery
                {"multi_match" : {
                    
                    "query": search_term, 
                    #and operator interprets our search term as a match_phrase query 
                    "operator" : "and" 
                    } },
            
             

                #must 2 filter phase
                 #term query and keyword fields dont get tokenized in search
                 { "terms": { "phase.keyword": phase_term}},


                #must 3 filter status                  
                 #term query and keyword fields dont get tokenized in search
                 { "terms": { "overall_status.keyword": status_term }},
                 
                
                #must 4 filter by disease ID
                #disease Id gecheckt
                { "multi_match":{ 
                       
                       "query": disease_id,
                       "operator": "or",
                       "fields": "occuring-Disease.annotation.infon.#text"
              
     
            
                                 }
                }
                     
                                        ]
              
              
              }
            }
           }
     )

     #5 SEarch und Disease  und Gene  
     if(disease_id != "" and search_term != "" and gene_id != ""):
         res = es.search(
       
          index= index,  

          body={       
              "from":hits_from, 
              "size": 5,
              "query": {
                  
                  "bool": {   

                      
                       "must": [
                          

                #must1 searchquery
                {"multi_match" : {
                    
                    "query": search_term, 
                    #and operator interprets our search term as a match_phrase query 
                    "operator" : "and" 
                    } },
            
             

                #must 2 filter phase
                 #term query and keyword fields dont get tokenized in search
                 { "terms": { "phase.keyword": phase_term}},


                #must 3 filter status                  
                 #term query and keyword fields dont get tokenized in search
                 { "terms": { "overall_status.keyword": status_term }},
                 
                
                #must 4 filter by disease ID
                #disease Id gecheckt
               
                
                { "multi_match":{ 
                       
                       "query":gene_id ,
                       "operator": "or",
                       "fields": "occuring-Gene.annotation.infon.#text"
              
                   },
            
                                 
                       "multi_match":{ 
                       
                       "query":disease_id ,
                       "operator": "or",
                           "fields": "occuring-Disease.annotation.infon.#text"
                       }}
                  
                
                
                     
                                                             ]
              
              
              }
            }
           }
        )
    #6 GeneID     
     if(disease_id == "" and search_term == "" and gene_id != ""):
        
       res = es.search(
        index=index ,

        body={
            
            "query": {
                              
                     "multi_match":{ 
                       
                       "query":gene_id ,
                       "operator": "or",
                       "fields": "occuring-Gene.annotation.infon.#text"
              
     
            
                                 }
                
            }
        }
    )   
   
    #7 Search und GeneID
     if(disease_id == "" and search_term != "" and gene_id != ""):
            
      res = es.search(
       
          index= index,  

          body={       
              "from":hits_from, 
              "size": 5,
              "query": {
                  
                  "bool": {   

                      
                       "must": [
                          

                #must1 searchquery
                {"multi_match" : {
                    
                    "query": search_term, 
                    #and operator interprets our search term as a match_phrase query 
                    "operator" : "and" 
                    } },
            
             

                #must 2 filter phase
                 #term query and keyword fields dont get tokenized in search
                 { "terms": { "phase.keyword": phase_term}},


                #must 3 filter status                  
                 #term query and keyword fields dont get tokenized in search
                 { "terms": { "overall_status.keyword": status_term }},
                 
                
                #must 4 filter by disease ID
                #disease Id gecheckt
               
                
                
                  { "multi_match":{ 
                
             
                       
                       "query": gene_id ,
                       "operator": "or",
                       "fields": "occuring-Gene.annotation.infon.#text"
                        
     
                     }
                                 }
                
                
                     
                                                             ]
              
              
              }
            }
           }
        )
        #8 GeneID and diseaseID    
     if(disease_id !="" and search_term == "" and gene_id != ""):
        
       res = es.search(
        index=index ,

        body={
            
            "query": {
                              
                   { "multi_match":{ 
                       
                       "query":gene_id ,
                       "operator": "or",
                       "fields": "occuring-Gene.annotation.infon.#text"
              
                   },
            
                                 
                       "multi_match":{ 
                       
                       "query":disease_id ,
                       "operator": "or",
                           "fields": "occuring-Disease.annotation.infon.#text"
                       }}
            
        } }
    )
    
     
     return res


#Rendering the homepage // setting route to our search page
@app.route('/')
def home():
   
 return render_template('results.html')

# Defining the home pageFIRST of our site
@app.route('/results', methods=['POST', 'GET'])  # this sets the route to results page
def search_request():

    
    
    search_term = request.form["search_term"]
    #print(request.form["search_term"])
    phase_term= request.form.getlist("mycheckbox")
   
    #print(phase_term)
    status_term= request.form.getlist("mycheckbox2")
    #print(status_term)

    disease_id = request.form["disease_id"]
    gene_id = request.form["gene_id"]

    #sole purpose richtigen display
    phase_default = ['N/A', 'Phase 1', 'Phase 2', 'Phase 3', 'Phase 4', 'Early Phase 1', 'Phase 1/Phase 2', 'Phase 2/Phase 3']
    status_default = ['Completed', 'Not yet recruiting', 'Active, not recruiting', 'Terminated', 'Enrolling by invitation', 'Withdrawn', 'Unknown status', 'Recruiting', 'No Longer available', 'Available', 'Withheld']
    
    phase_checked = phase_default.copy()
    status_checked= status_default.copy()
    
    # MARK checked Phase
    for i in range(len(phase_checked)):
        if phase_checked[i] in phase_term :
            phase_checked[i] ='checked'
        else :
            phase_checked[i] = ''

   # MARK checked status 
    for i in range(len(status_checked)):
        if status_checked[i] in status_term :
            status_checked[i] ='checked'
        else :
            status_checked[i] = ''

    if not phase_term :
        phase_term = phase_default
    if not status_term :    
        status_term= status_default
    ####   
    
    RESULTS_PER_PAGE= 5 

    
  
    hits_from=0 
    
    
    current_page = 1
    num_pages = None
  



    if (disease_id != "" or search_term != "" or gene_id !=""):
              
           
            
              
              hits_from = int(request.form.get("hits_from",0))
              print(hits_from)
              res= es_body(search_term, disease_id,gene_id, phase_term, status_term, hits_from, RESULTS_PER_PAGE)
 
              total_hits = res["hits"]["total"]["value"]
                   # Prüfe, ob wir auf der letzen Seite angekommen sind
  

              num_pages = math.ceil( total_hits / RESULTS_PER_PAGE)
              current_page = int(hits_from / RESULTS_PER_PAGE + 1)
        
    else :
          total_hits= -1
          res=[]

    
    return render_template(
       'results.html',
        res=res,
        search_term=search_term, 
        phase_term=phase_term, 
        phase_checked=phase_checked,
        status_term=status_term, 
        status_checked=status_checked,
        disease_id= disease_id, 
        gene_id=gene_id,
        hits_from = hits_from , 
        total_hits=total_hits,
        current_page=current_page,
        num_pages=num_pages,
        num_results_per_page=RESULTS_PER_PAGE )
#######################################################################

#################################################################################
#Routing detailpage
@app.route("/resultsdetail/<rnk>")
def singular(rnk):
    res = es.search(
        index=index, #insert index name

        body={
            
            "query": {
                "match" : {
                    "id_info.nct_id":rnk
                    
                    
                   
                }
            }
        }
    )
   
   #extracting diseases 
    getdis = es.search(
        index= index, #insert index name

        body={
            "_source" : ["occuringCounts-Disease.Disease.name" , "occuringCounts-Disease.Disease.count", "occuringCounts-Disease.Disease.standarizedtag"] ,
            "query": {
                "match" : {
                    "id_info.nct_id":rnk
                    
                   
                }
            }
        }
    )



    #extracting genes 
    getgene = es.search(
        index= index, #insert index name

        body={
            "_source" :  ["occuringCounts-Gene.Gene.name",  "occuringCounts-Gene.Gene.count", "occuringCounts-Gene.Gene.standarizedtag"] ,
            "query": {
                "match" : {
                    "id_info.nct_id":rnk
                    
                   
                }
            }
        }
    )


    return render_template('einzeln.html',res=res , getdis=getdis, getgene= getgene )





###############################################################


#Running the app in main() by default:
if __name__ == '__main__' :
    app.run(debug=True, port =5000)








   
                     