import os
from suffix_rules import INFLECTIONAL_SUFFIXES, DERIVATIONAL_SUFFIXES, normalize_word


ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kok_listesi.dict")
if not os.path.exists(ROOT_PATH):
    alt_path = os.path.join(os.getcwd(), "turkish_stemmer_snowball/kok_listesi.dict")
    if os.path.exists(alt_path):
        ROOT_PATH = alt_path

try:
    with open(ROOT_PATH, encoding="utf-8") as f:
        ROOTS = {normalize_word(line.strip()) for line in f if line.strip()}
    print(f"Loaded {len(ROOTS)} roots from {ROOT_PATH}.")
except FileNotFoundError:
    ROOTS = set()
    print("Warning: root dictionary not found; ROOTS set empty.")


def repair_final_consonant(stem: str) -> str:
    if stem in ROOTS or not stem:
        return stem
    if stem.endswith("tt") and stem[:-1] in ROOTS:
        return stem[:-1]
    if stem.endswith("kk") and stem[:-1] in ROOTS:
        return stem[:-1]
    if stem.endswith("b"):
        return stem[:-1] + "p"
    if stem.endswith("d"):
        return stem[:-1] + "t"
    if stem.endswith("ğ"):
        return stem[:-1] + "k"
    return stem


def repair_vowel_change(stem: str) -> str:
    mapping = {
        "söylü": "söyle", "söyl": "söyle",
        "başlı": "başla", "bekli": "bekle",
        "alı": "al", "yazı": "yaz", "kalkı": "kalk",
        "yapı": "yap", "görü": "gör", "gelü": "gel", "gidü": "git"
    }
    for patt, corr in mapping.items():
        if stem.startswith(patt):
            return corr
    return stem


def _prefer_longer_root(original_word: str, before_strip: str, after_strip: str):
    cand = normalize_word(after_strip)
    if cand not in ROOTS:
        return after_strip
    if original_word.endswith(("tı", "ti", "tu", "tü")):
        plus_t = cand + "t"
        if plus_t in ROOTS:
            return plus_t
    if original_word.endswith(("dı", "di", "du", "dü")):
        plus_d = cand + "d"
        if plus_d in ROOTS:
            return plus_d
    return after_strip


def strip_suffix(word: str, suffixes: list[str], min_len: int = 2, single_pass: bool = False):
    word = normalize_word(word)
    prev = None
    removed = []

    if word in ROOTS:
        return word, []

    while word != prev:
        prev = word
        for suf in suffixes:
            if len(suf) in (1, 2):
                if word.endswith("t") and normalize_word(word) in ROOTS:
                    continue
            if word.endswith(suf) and len(word) - len(suf) >= min_len:
                candidate = word[:-len(suf)]

                if suf in {"mak", "mek"}:
                    if candidate in {"et", "ol", "yap"}:
                        return candidate, removed + [suf]
                    word = candidate
                    removed.append(suf)
                    break

                if suf in {"ma", "me"}:
                    if not any(word.endswith(x) for x in ["sma", "rma", "kma", "nma", "pma", "tma", "çma"]):
                        word = candidate
                        removed.append(suf)
                        continue

                norm_cand = normalize_word(candidate)
                if norm_cand in ROOTS:
                    better = _prefer_longer_root(word, word, candidate)
                    return normalize_word(better), removed + [suf]

                word = candidate
                removed.append(suf)
                if single_pass:
                    return word, removed
                break
    return word, removed


STEM_FIXES = {
    "gerektik": "gerek", "gerekti": "gerek", "gerektiği": "gerek", "gerekmek": "gerek",
    "bulunduk": "bulun", "bulundu": "bulun", "bulundum": "bulun",
    "olundu": "ol", "olunduk": "ol",
    "yapıldı": "yap", "yapıldık": "yap",
    "denildi": "de", "denildik": "de",
    "göründü": "gör", "göründük": "gör",
    "bilindi": "bil", "bilindik": "bil",
    "gidildi": "git", "gidildik": "git",
    "verildi": "ver", "verildik": "ver",
    "yazıldı": "yaz", "yazıldık": "yaz",
    "edildi": "et", "edildik": "et",
    "düşünüldü": "düşün", "düşünüldük": "düşün",
    "seçildi": "seç", "seçildik": "seç",
    "beklendi": "bekle", "beklendik": "bekle",
    "gelindi": "gel", "gelindik": "gel",
    "bulunuldu": "bulun", "di": "de", "diy": "de", "yiy": "ye"
}


def stem_word(word: str, debug: bool = False) -> str:
    word = normalize_word(word)
    if word in ROOTS:
        return word

    stem1, _ = strip_suffix(word, INFLECTIONAL_SUFFIXES, min_len=2)
    stem2, _ = strip_suffix(stem1, DERIVATIONAL_SUFFIXES, min_len=3)

    if stem2 in ROOTS:
        final_stem = stem2
    else:
        repaired_vowel = repair_vowel_change(stem2)
        if repaired_vowel in ROOTS:
            final_stem = repaired_vowel
        else:
            repaired = repair_final_consonant(stem2)
            if repaired in ROOTS:
                final_stem = repaired
            else:
                repaired2, _ = strip_suffix(repaired, DERIVATIONAL_SUFFIXES, min_len=3)
                final_stem = repaired2 if repaired2 in ROOTS else repair_final_consonant(stem2)

    if final_stem in STEM_FIXES:
        final_stem = STEM_FIXES[final_stem]

    return final_stem
