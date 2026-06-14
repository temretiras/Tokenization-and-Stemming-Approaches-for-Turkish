import xml.etree.ElementTree as ET
import os
import sys

def extract_mwes_from_all_xmls(directory_path):
    """
    Scan every *_wordnet.xml file under the directory and collect
    every unique multi-word expression.
    """
    
    total_mwes = set()
    
    print(f"Scanning XML files under '{directory_path}'")
    
    try:
        files_in_directory = os.listdir(directory_path)
    except FileNotFoundError:
        print(f"ERROR: directory '{directory_path}' was not found.", file=sys.stderr)
        print("Tip: ensure the Kenet folder is next to this script.", file=sys.stderr)
        return []
    except Exception as e:
        print(f"ERROR: could not read directory: {e}", file=sys.stderr)
        return []

    xml_files_to_process = [f for f in files_in_directory if f.endswith("_wordnet.xml")]
    
    if not xml_files_to_process:
        print(f"ERROR: no *_wordnet.xml files found under '{directory_path}'.", file=sys.stderr)
        return []

    print(f"Found {len(xml_files_to_process)} XML files:")
    for f in xml_files_to_process:
        print(f"  - {f}")

    for xml_file in xml_files_to_process:
        xml_path = os.path.join(directory_path, xml_file)
        
        print(f"\n--- Processing: {xml_path} ---")
        
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            found_in_this_file = 0
            for literal in root.findall(".//{*}LITERAL"):
                if literal.text and " " in literal.text:
                    mwe = literal.text.strip()
                    if mwe not in total_mwes:
                        total_mwes.add(mwe)
                        found_in_this_file += 1
            
            print(f"Added {found_in_this_file} new MWEs from this file.")
            
        except ET.ParseError:
            print(f"WARNING: {xml_file} could not be parsed. Skipping.", file=sys.stderr)
        except Exception as e:
            print(f"WARNING: {xml_file} failed: {e}. Skipping.", file=sys.stderr)

    print("\nFinished scanning all files.")
    
    return sorted(list(total_mwes))

xml_folder = "turkish-tokenizer-rb"
mwe_list = extract_mwes_from_all_xmls(xml_folder)

if mwe_list:
    print(f"\nCollected {len(mwe_list)} unique MWEs.")
    
    output_filename = "trmwe_list.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        for mwe in mwe_list:
            f.write(mwe + "\n")
            
    print(f"\nSaved the list to '{output_filename}'.")
    
    print("\n--- Sample MWEs ---")
    for mwe in mwe_list[:20]:
        print(mwe)
else:
    print(f"\nNo MWEs found under '{xml_folder}' or the files were unreadable.")
