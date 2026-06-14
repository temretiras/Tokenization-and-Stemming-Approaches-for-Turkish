from suffix_rules import normalize_word


def load_conllu_pairs(path, limit=None):
    """
    Reads word–lemma pairs from a CoNLL-U file.
    Skips AUX tokens.
    Returns two lists: words and lemmas.
    If a limit is set, reads only the first N pairs.
    Lemmas are normalized for consistent evaluation.
    """
    words, lemmas = [], []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.strip().split("\t")
            if len(parts) > 3:
                word, lemma, upos = parts[1], parts[2], parts[3]
                if upos == "AUX":
                    continue
                if lemma != "_" and word.isalpha():
                    words.append(word)
                    lemmas.append(normalize_word(lemma))
                    if limit and len(words) >= limit:
                        break

    print(f"Loaded {len(words)} word–lemma pairs from {path} (AUX excluded).")
    return words, lemmas
