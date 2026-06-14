#!/usr/bin/env python
# coding: utf-8

"""
Kenet (Türkçe WordNet) XML Ayrıştırıcısı. (DÜZELTİLMİŞ v3 - MWE Filtreli)

Bu script, 'turkish*_wordnet.xml' kalıbıyla eşleşen tüm Kenet XML dosyalarını
kendi bulunduğu dizinde tarar. İçlerindeki <LITERAL> etiketlerini çıkarır.

YENİ: Boşluk içeren (örn: "göz atmak") deyimleri (MWEs) yoksayar.
YENİ: Fiilse (örn: "gitmek"), hem mastar halini hem de kök halini ("git") ekler.
"""

import xml.etree.ElementTree as ET
import glob
import os
import sys

# --- Script'in kendi dizinini bul ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# XML dosyalarını script'in kendi dizininde ara
XML_FILE_PATTERN = os.path.join(SCRIPT_DIR, 'turkish*_wordnet.xml')

# Çıktı dosyasını bir üst dizine (ana proje dizinine) yaz
OUTPUT_FILENAME = os.path.join(SCRIPT_DIR, '..', 'kenet_kokler.py')


def build_kenet_lexicon():
    print(f"Kenet (Türkçe WordNet) kök listesi oluşturuluyor...")
    
    xml_files = glob.glob(XML_FILE_PATTERN)
    
    if not xml_files:
        print(f"HATA: Hiçbir dosya bulunamadı.")
        print(f"       Aranan dizin: {SCRIPT_DIR}")
        print(f"       Aranan kalıp: {XML_FILE_PATTERN}")
        sys.exit(1) # Hata kodu 1

    all_lemmas = set()
    total_files = 0
    mwe_skipped_count = 0

    for filepath in xml_files:
        print(f"İşleniyor: {filepath}...")
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            literals = root.findall('.//LITERAL')
            
            file_lemma_count = 0
            file_verb_stems_added = 0
            for literal in literals:
                lemma = literal.text
                if lemma:
                    lemma_clean = lemma.strip().lower()
                    
                    # --- YENİ FİLTRE (DEYİM/MWE KONTROLÜ) ---
                    # Eğer kök bir boşluk içeriyorsa (örn: "göz atmak"),
                    # bu bir deyimdir (MWE) ve stemmer'ın kök listesine GİRMEMELİDİR.
                    if lemma_clean and ' ' not in lemma_clean:
                    # ----------------------------------------

                        # 1. Kökün kendisini ekle (örn: 'gitmek')
                        all_lemmas.add(lemma_clean)
                        file_lemma_count += 1
                        
                        # 2. Eğer fiilse, mastarsız halini de ekle
                        if lemma_clean.endswith('mek'):
                            all_lemmas.add(lemma_clean[:-3]) # 'git'
                            file_verb_stems_added += 1
                        elif lemma_clean.endswith('mak'):
                            all_lemmas.add(lemma_clean[:-3]) # 'oku'
                            file_verb_stems_added += 1
                    
                    elif ' ' in lemma_clean:
                        mwe_skipped_count += 1
                        
            print(f" -> {file_lemma_count} kök ve {file_verb_stems_added} fiil gövdesi eklendi.")

        except ET.ParseError as e:
            print(f"UYARI: {filepath} ayrıştırılırken XML hatası (atlandı): {e}")
        except Exception as e:
            print(f"HATA: {filepath} işlenirken bilinmeyen hata (atlandı): {e}")

    print(f"\nİşlem tamamlandı. Toplam {total_files} XML dosyası işlendi.")
    print(f"Bulunan toplam benzersiz kök (KOKLER): {len(all_lemmas)}")
    print(f"Yoksayılan Deyim/MWE sayısı: {mwe_skipped_count}")

    # --- Dosyayı Yazma ---
    print(f"'{OUTPUT_FILENAME}' dosyası yazılıyor...")
    try:
        with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
            f.write("#!/usr/bin/env python\n")
            f.write("# coding: utf-8\n\n")
            f.write(f"# Bu dosya, 'kenet_parser.py' tarafından otomatik olarak oluşturulmuştur.\n")
            f.write("# MANUAL OLARAK DÜZENLEMEYİN.\n\n")
            
            f.write(f"KOKLER = {{\n")
            for kok in sorted(all_lemmas):
                f.write(f"    {repr(kok)},\n")
            f.write("}\n")
            
        print(f"\nBaşarıyla oluşturuldu: {OUTPUT_FILENAME}")
        
    except Exception as e:
        print(f"HATA: {OUTPUT_FILENAME} dosyası yazılırken sorun oluştu: {e}")

if __name__ == "__main__":
    build_kenet_lexicon()