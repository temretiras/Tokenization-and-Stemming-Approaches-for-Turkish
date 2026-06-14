import pyconll
from zemberek import TurkishMorphology
import re

morphology = TurkishMorphology.create_with_defaults()

INPUT_CONLLU = "/home/toroscanavari/Documents/cmpe561/applproject1/tr_boun-ud-train.conllu"
OUTPUT_FILE = "lemmas_from_conllu.txt"

def parse_lemma(analysis_str: str):
    """
    Extract the surface lemma from a Zemberek analysis string.
    """
    match = re.search(r"\]\s*([\wçğıöşüÇĞİÖŞÜ\-]+):", analysis_str)
    if match:
        return match.group(1)
    return None

def zemberek_lemma(word: str) -> str:
    if not word.strip():
        return ""
    results = morphology.analyze_and_disambiguate(word).best_analysis()
    if not results:
        return ""
    analysis_str = str(results[0])
    lemma = parse_lemma(analysis_str)
    return lemma if lemma else ""

def main():
    dataset = pyconll.load_from_file(INPUT_CONLLU)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as fout:
        for sent in dataset:
            for token in sent:
                # sadece normal token'ları al, multiword token'ları atla
                if "-" in token.id or "." in token.id:
                    continue
                form = token.form
                lemma = zemberek_lemma(form)
                fout.write(lemma + "\n")

    print(f"Lemmas saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
