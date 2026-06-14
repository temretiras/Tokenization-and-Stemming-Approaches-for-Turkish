import difflib
import unicodedata
from stemmer_debuggable import stem_word


def normalize_unicode(s: str) -> str:
    """Normalize string to lowercase NFC form and remove dotted variants."""
    if not isinstance(s, str):
        return s
    s = s.strip().lower()
    s = unicodedata.normalize("NFKC", s)
    s = unicodedata.normalize("NFC", s)
    s = s.replace("ı̇", "i").replace("i̇", "i")
    return s


def evaluate_dual(words, lemmas, tolerance=0.7, export_path=None):
    """
    Evaluate stemmer performance in two modes:
      1. Strict accuracy: exact match after Unicode normalization.
      2. Soft accuracy: edit similarity is equal to or bigger than tolerance.
    """
    total = len(words)
    strict_correct = 0
    soft_correct = 0
    results = []

    for w, l in zip(words, lemmas):
        result = stem_word(w, debug=False)
        stem = result[0] if isinstance(result, (tuple, list)) else result
        sim = difflib.SequenceMatcher(None, normalize_unicode(stem), normalize_unicode(l)).ratio()

        strict_match = normalize_unicode(stem) == normalize_unicode(l)
        soft_match = strict_match or (sim >= tolerance)

        if strict_match:
            strict_correct += 1
        if soft_match:
            soft_correct += 1

        results.append({
            "word": w,
            "stem": stem,
            "lemma": l,
            "similarity": round(sim, 3),
            "strict": strict_match,
            "soft": soft_match,
        })

    strict_acc = strict_correct / total * 100
    soft_acc = soft_correct / total * 100

    print("\nStemmer Evaluation Results (Unicode-normalized)")
    print("-" * 65)
    print(f"{'Total tokens':25s}: {total}")
    print(f"{'Strict accuracy':25s}: {strict_acc:.2f}% ({strict_correct}/{total})")
    print(f"{'Soft accuracy (≥'+str(tolerance)+')':25s}: {soft_acc:.2f}% ({soft_correct}/{total})")
    print("-" * 65)

    if export_path:
        import csv
        with open(export_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"Detailed results saved to {export_path}\n")

    return strict_acc, soft_acc
