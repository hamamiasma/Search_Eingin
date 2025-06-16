Vielen Dank dass Sie sich für Baymax entschieden haben! 

Inhalt
1. Installationsanleitung
2. Konfigurierung über config.ini
3. Ausführung
4. Separate Nutzung der Annotations-Module
5. Trouble-Shooting
6. Credits


1. Installationsanleitung

Bitte beachten Sie: Diese Anwendung funktioniert nur auf linuxbasierenden Systemen.

1. Sämtliche benötigten Module können über die Konsole mittels 'python -m pip install -r requirements.txt‘ installiert werden.
2. Erstellen Sie einen Ordner in dem sämtliche zur Anwendung gehörigen Ressources abgelegt werden.
3. Laden Sie GNorm über die Konsole mit 'wget https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/download/GNormPlus/GNormPlusJava.zip' herunter
4. Entpacken Sie die zip-Datei in den Ordner aus Schritt 2 mit 'unzip GNormPlusJava.zip'.
5. Führen Sie das Installationsskript ("sh Installation.sh") im GNorm-Verzeichnis aus. Wenn es zu Problemen kommt, finden Sie weitere Hinweise unter "5. Trouble-Shooting" unten, oder in der ReadMe von GNormPlus.
6. Überprüfen Sie die Funktionalität von GNormPlus. Kopieren sie hierzu die "testBioC.xml" in den "input"-Ordner im GNormPlus-Verzeichnis.
Starten Sie GNorm im GNormPlus-Verzeichnis mit dem Terminal-Befehl: "java -Xmx10G -Xms10G -jar GNormPlus.jar input output setup.txt". Sollte es zu Problemen kommen, finden Sie weitere Hinweise unter "5. Trouble-Shooting".
7. Laden Sie DNorm über die Konsole mit 'wget https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/tmTools/download/DNorm/DNorm-0.0.7.tgz' herunter
8. Entpacken Sie die tar-Datei in den Ordner aus Schritt 2. Weitere Installationsschritte wie bei GNormPlus sind nicht erforderlich.
9. Überprüfen Sie die Funktionalität von DNorm. Kopieren sie hierzu die "testBioC.xml" in den "input"-Ordner im DNorm-Verzeichnis.
Starten Sie DNorm im DNorm-Verzeichnis mit dem Terminal-Befehl: "./RunDNorm_BioC.sh config/banner_NCBIDisease_TEST.xml data/CTD_diseases.tsv output/simmatrix_NCBIDisease_e4.bin sample.txt sample-out2.txt". Sollte es zu Problemen kommen, finden Sie weitere Hinweise unter "5. Trouble-Shooting".
10. Clonen Sie das Repository über die Konsole mit 'git clone git@gitlab.informatik.hu-berlin.de:ws21-22_semesterprojekt-5/scrum-team-1.git' im den Ordner aus Schritt 2
11. Laden Sie Elasticsearch über die Konsole mit 'wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.15.2-linux-x86_64.tar.gz'
   herunter
12. Entpacken Sie die tar-Datei im Ordner aus Schritt 2 mit 'tar -xzf elasticsearch-7.15.2-linux-x86_64.tar.gz'
13. Laden Sie über die Konsole mit'wget https://artifacts.elastic.co/downloads/kibana/kibana-7.17.0-linux-x86_64.tar.gz' herunter
14. Entpacken Sie die tar-Datei im Ordner aus Schritt 2 mit 'tar -xzf kibana-7.17.0-linux-x86_64.tar.gz'
15. Prüfen Sie in der config.ini ob sämtliche benögtigten Unterordner angegeben sind. Hinweise dazu finden Sie im nächsten Abschnitt

Wenn Sie mit allen Schritten fertig sind müsste Ihr Verzeichnis wie folgt strukturiert sein:
- meinSchritt2Ordner
   - GNormPlus
   - DNorm
   - elasticsearch-7.15.2
   - kibana-7.15.1
   - scrum-team-1
      - baymaxbackbone.py
      - config.ini
      - Webapp
         -server.py


2. Konfigurierung über config.ini

Vor der Nutzung von Baymax müssen Sie die config-Datei anpassen. Für die standardmäßige Nutzung von Baymax über das "baymaxbackbone" Skript (Siehe 3. Ausführung) sind nur die Pfade unter "Start" (in der config.ini) wichtig. 
Folgende Pfade sind anzugeben:
path_to_originals : Pfad zum Oberverzeichnis der Studien. Alle XML-Dateien die sich (bei beliebiger Ordnerstruktur und Ordnertiefe der Dateien) in diesem Verzeichnis befinden, werden von Baymax verarbeitet. Hier liegen also alle Dateien die in Elasticsearch indexiert, oder die zuerst mit NLP-Tags annotiert und danach indexiert werden sollen. Stellen Sie sicher,dass alle XML-Files im Format von clinical-trails.gov sind.

path_to_resources : Pfad zum Ordner in dem sich sämtliche zum Projekt gehörigen Files befinden, sprich der Ordner aus Schritt 2

path_to_python    : Pfad unter dem die python.exe zu finden ist

index             : Name des Zielindex in elastic-search. Dieses Feld muss nur angepasst werden, wenn Baymax ausschließlich für einen bereits bestehenden Index die WebApp starten soll (siehe 3. Ausführung - Option 0). In allen anderen Fällen wird der Index durch Konsoleneingabe des Nutzers während der Ausführung festgelegt und dann automatisch hier reingeschrieben.

!ACHTUNG!
Wichtig ist, dass alle Pfade mit "/" enden. 


3. Ausführung

Starten Sie das Python-Skript "baymaxbackbone.py" im Terminal.
Sie werden dann aufgefordert über Eingabe einer Ziffer 0 bis 4 Ihre gewünschte Baymax-Funktion zu starten.

!ACHTUNG!
Starten Sie noch nicht Elasticsearch und Kibana! Baymax wird Ihnen mitteilen wann dies geschehen soll. Anderfalls kann es bei der Ausführung des Annotationsprozesses zu Systemüberlastungen kommen, da insbesondere Elasticsearch und GNorm viele Ressourcen benötigen.
Wenn Sie Elasticsearch & Kibana gestartet haben, stellen Sie sicher, dass beide Anwendungen vollständig geladen sind, indem sie localhost:5601 aufrufen bis das Kibana-Interface erfolgreich im Browser geladen ist. Setzen Sie erst dann die Ausführung von Baymax wie gefordert fort.

3.1. Baymax-Funktionen

Option 0
Diese Option starten lediglich die WebApp für einen in der config.ini hinterlegten Elastic-Search-Index (siehe 3.2. WebApp).

Option 1
Sie werden aufgefordert einen Ziel-Index anzugeben (dieser wird dann in die config.ini geschrieben). 
Alle Studien unter path_to_originals werden dann direkt - ohne Natural Language PreProcessing - in Elasticsearch indexiert.
Diese Option ist dafür gedacht, wenn Sie eine bereits annotierten Satz Studien vorgegeben haben oder die Annotations-Module manuell genutzt haben (Siehe und 4. Separate Nutzung der Annotations-Module) und die bereits annotierten Studien indexieren wollen.
Nach der Indexierung wird direkt die WebApp gestartet (siehe 3.2. WebApp).

Option 2
Sie werden aufgefordert einen Ziel-Index anzugeben (dieser wird dann in die config.ini geschrieben). 
Alle Studien unter path_to_originals werden unter Nutzung von GNormPlus annotiert (mit Gen- und Species-Tags) und anschließend in Elasticsearch indexiert.
Nach der Indexierung wird direkt die WebApp gestartet (siehe 3.2. WebApp).

Option 3
Sie werden aufgefordert einen Ziel-Index anzugeben (dieser wird dann in die config.ini geschrieben). 
Alle Studien unter path_to_originals werden unter Nutzung von DNorm annotiert (mit Disease-Tags) und anschließend in Elasticsearch indexiert.
Nach der Indexierung wird direkt die WebApp gestartet (siehe 3.2. WebApp).

Option 4
Sie werden aufgefordert einen Ziel-Index anzugeben (dieser wird dann in die config.ini geschrieben). 
Alle Studien unter path_to_originals werden unter Nutzung von GNormPlus und DNorm annotiert (mit Gen-, Species-, Disease-Tags) und anschließend in Elasticsearch indexiert.
Nach der Indexierung wird direkt die WebApp gestartet (siehe 3.2. WebApp).

!ACHTUNG!
Beachten Sie, dass der Annotations und Indexierungs-Prozess Recourcen- und Zeitintensiv sein kann, insbesondere für größere Mengen an zu verarbeitenden Studien. Die größten Zeitfresser sind GNormPlus und in kleinerem Maße, DNorm und der Indexierer. Unter 5. Trouble-Shooting finden sie weitere Hinweise.

3.2.WebApp
Die WebApp ist unter localhost:5000 zu erreichen, kibana unter localhost:5601
In der Web-oberfläche können Sie verschiedene Filter nutzen und über die gesonderten Suchfelder für Gene und Krankheiten (Diseases) gezielt unter Eingabe der gewünschten NCBI-Tags (Gene), oder MESH-IDs (Krankheiten) nach gewünschten Entitäten suchen.

Zum Beenden der WebApp müssen Sie im Terminal wo die Anwendung läuft, diese manuell via strg+c schließen.


4. Separate Nutzung der Annotations-Module
Sollten Sie die Funktionalität von baymaxbackbone nicht nutzen können oder wollen, ist es möglich die einzelnen Backendmodule einzeln zu nutzen. Hierfür müssen die Pfade unter "PREPROCESSING" in der config.ini korrekt gesetzt sei (s.u.)

Die Preprocess-Pipeline ist wie folgt aufgebaut:

4.1. biocConverter.py 
Dieses direkt ausführbare Skript erstellt für die unter path_to_study_orignals gefundenen XML (Ordner wird rekursiv durchsucht) jeweils passende XML-Files im BioC Format und speichert die unter path_to_reduced_studies_in_bioc_xml. Dieses Format wird von DNorm & GNorm verlangt. Es handelt sich um ein flexibles, einfaches Format zum Informationsaustausch in der BioInformatik. 
Weitere Informationen finden Sie hier: http://bioc.sourceforge.net

4.2. GNormPlus
Navigieren Sie im Terminal ins GNormPlus-Verzeichnis und führend Sie dort den Befehl:
"java -Xmx10G -Xms10G -jar GNormPlus.jar input output setup.txt"
aus. Die Felder müssen sie ggf. durch passende Pfade ersetzen z.B. wenn der input direkt aus dem unter path_to_reduced_studies_in_bioc_xml hinterlegten Pfad kommen sollen (also die in 4.1. erzeugten BioC-Files). 

4.3. DNorm
Navigieren Sie im Terminal ins DNorm-Verzeichnis und führend Sie dort den Befehl:
"./RunDNorm_BioC.sh config/banner_NCBIDisease_TEST.xml data/CTD_diseases.tsv output/simmatrix_NCBIDisease_e4.bin input outputfiles"
aus. Die Felder input & outputfiles müssen sie ggf. durch passende Pfade ersetzen
Benutzen sie NICHT den ordner output, dort werden verschiedene resourcen von DNorm gespeichert!

4.4. integrateAnnotation.py
Dieses direkt ausführbare Skript nimmt die unter path_to_nlp_pipeline_outputs gefunden XML-Files, die alle (mit DNorm/GNormPlus) annotierte BioC-XML-Files sein müssen und versucht die gefundenen Annotationen in die unter path_to_study_orignals hinterlegten Studien-Originale zu integrieren. Die Ergebnisse werden nach path_to_integrated_studies geschrieben.

Die nun annotierten Studien können mittels baymaxbackbone - Option 1 (siehe 3. Ausführung) in Elasticsearch indexiert werden.

Übersicht über die benötigten Einträge in der config.ini:
   path_to_study_orignals              : Pfad zu den originalen Studien
   path_to_nlp_pipeline_outputs        : Pfad zu den von GNorm und/oder DNorm annotierten Studien
   path_to_integrated_studies          : Zielpfad für integrateAnnotation.py
   path_to_reduced_studies_in_bioc_xml : Zielpfad für biocConverter.py


5. Trouble-Shooting

GNormPlus-Installation/läuft nicht
-Wenn die Installations nicht erfolgreich war/der Funktionitätstest fehlschlägt, müssen Sie vermutlich CRF++ manuell neu installieren. Nutzen Sie hierfür die Hinweise aus der readme von GNorm:

If failed by using Installation.sh, please reinstall CRF++ by below steps:
			
			1) Download CRF++-0.58.tar.gz from https://drive.google.com/folderview?id=0B4y35FiV1wh7fngteFhHQUN2Y1B5eUJBNHZUemJYQV9VWlBUb3JlX0xBdWVZTWtSbVBneU0&usp=drive_web#list
			2) Uncompress the file by 
			
				$ tar -zxvf CRF++-0.58.tar.gz

			3) Move all files and folders under CRF++-0.58 to the [CRF] folder.

			4) Execute below instructions in CRF folder.
				$ ./configure 
				$ make
				$ su
				$ make install

-Es kann sein dass für GNormPlus das Programm Ab3P die Anwendungsrechte freigegeben werden müssen. Dies ist über die Konsole mit dem Befehl chmod u+x Ab3P

DNorm-instsllation/retraining
DNorm benötigt auch CRF++was evt. manuell reinstalliert werden muss. Siehe hierfürdie obigen Hinweise zu Troubleshooting-GNormPlus!
In der ReadMe von DNorm finden Sie Hinweise für eventuelle Probleme (sowie Anleitungen DNorm neu zu trainieren und zu bewerten, was für die Nutzung von Baymax nicht notwendig ist).

Zeitverbrauch
GNorm schafft auf einem Heimrechner ca. 1 Studie pro sekunde. Bei größerem Studien-Input kommt es manchmal nach einer Weile zu einer Verlangsamung. Berücksichtigen Sie dies bei Wahl der Anzahl zu bearbeitender Studien. Prinzipiell sollten verschiedene BaymaxInstanzen auf verschiedenen Maschinen auf den Index schreiben können. Falls man GNorm manuell (ohne baymaxbackbone) aufruft, kann man außerdem den Prozess über Strg+C abbrechen, ggf. den Arbeitsspeicher bereinigen und dann GNorm neustarten. GNorm & Dnorm annotieren nur Dateien zu denen es im output-Ordner nboch keine entsprechung gibt.


6. Credits
Creators:
Asma Hamami
Clemens Paul
Johannes Brosz
Malak Hammam
