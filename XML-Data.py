import os
import pandas as pd
import xml.etree.ElementTree as ET

def getFiles():
    # Aktueller Pfad -> path
    path = os.getcwd()
    # Liste alle Daten im aktuellen Ordner auf -> files
    files = os.listdir(path=path)

    # Liste aller XML Files -> xml_files
    xml_files = [file for file in files if file.endswith(".xml")]
    # Ergebnis Rückgabe
    return xml_files

def parse_xml_tree(element, filename, parent=None):
    # 
    # Initiiere leere Liste "result"
    result = []
    # For-Loop über alle "child" eines "elements"
    for child in element:
        # Was zuerst True ist, wird zurückgegeben:
        # Falls das Tag ein Attribut "name" hat, sonst wird das Tag genutzt:
        tag_name = child.attrib.get('name') or child.tag
        # Die Value vom Attribut ist inital "None"
        value = None
        # Prüft, ob das elemet ein darunterliegendes Tag "wert" hat.
        # Falls ja -> wird die Variable "value" mit dem Wert aus dem Tag "wert" überschrieben
        # Falls nicht, wird geprüft ob das Tag selbst einen Wert besitzt, diese überschreibt dann auch die Variable "value"
        wert_child = child.find('wert')
        if wert_child is not None:
            value = wert_child.text.strip()
        elif child.text:
            value = child.text.strip()
        # Die Liste "result" wird mit den Tags und den Werten gefüllt, außerdem wird der Filename und Parent als extra Spalte ausgegeben.
        # Das erleichtert die Identifizierung in der Excel File später.
        # Aktuelle Datei -> filename
        # Oberpunkt des aktuellen Tags -> parent
        # Aktuelle Tags -> tag_name
        # Wert des aktuellen Tags -> value
        result.append({'filename': filename, 'parent': parent, 'tag': tag_name, 'value': value})
        
        if len(child) > 0 and wert_child is None:
            # Falls das aktuelle Tag ein child hat oder wert_child ist nicht None, dann wird es an das result angehängt
            # Unterpunkt des aktuellen Tags -> child
            # Aktuelle Datei -> filename
            # Aktuelles Tag -> parent
            result.extend(parse_xml_tree(child, filename, parent=tag_name))
    # Ergebnis Rückgabe
    return result

def getXML():
    # Alle XML-Files -> files
    files = getFiles()
    # Initiiere leere Liste "all_results"
    all_results = []
    # For-Loop über alle XML-Files
    for file in files:
        # Parse XML-File -> tree
        tree = ET.parse(file)
        # Findet die unterste Ebene von "tree" -> root
        root = tree.getroot()
        # Speichert den aktuelle Dateinamen -> filename
        filename = os.path.basename(file)
        # Führt die Funktion parse_xml_tree aus:
        result_list = parse_xml_tree(root, filename)
        # Speichert das Ergebnis der Funktion parse_xml_tree in der Liste "all_results"
        all_results.extend(result_list)
    # Die Liste "all_results" wird in ein DateFrame überführt
    df = pd.DataFrame(all_results)
    # Ergebnis Rückgabe
    return df

#result_df = main()
#result_df.to_excel("output.xlsx")
