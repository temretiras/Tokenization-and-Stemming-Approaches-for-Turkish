import sys
import csv
import pyconll
from rule_based_tokenizer import RuleBasedTokenizer

# FILE PATHS

KENET_PATH = "turkish-tokenizer-rb/tr_kenet-ud-train.conllu"
OUTPUT_CSV = "turkish-tokenizer-rb/tokenizer_error_analysis_REAL.csv"  # Output report path
ABBR_LIST_PATH = "turkish-tokenizer-rb/zemberek_abbreviations.txt" 

APPLY_LOWER = False

# TOKENIZER INITIALIZATION
try:
    tokenizer = RuleBasedTokenizer(
        abbreviations_path=ABBR_LIST_PATH,
        trmwe_list_path=''  # MWE list explicitly left blank
    )
except FileNotFoundError:
    print(f"ERROR: Abbreviation file not found at: {ABBR_LIST_PATH}", file=sys.stderr)
    tokenizer = RuleBasedTokenizer(trmwe_list_path='')
except Exception as e:
    print(f"Error during tokenizer initialization: {e}", file=sys.stderr)
    sys.exit(1)


# EVALUATION SCRIPT

header = [
    "sentence_id",
    "sentence_text",
    "gold_tokens",
    "pred_tokens",
    "missing_tokens",
    "extra_tokens",
    "exact_match",
    "token_accuracy",
]

rows = []

def jaccard_similarity(a, b):
    """Calculates the Jaccard similarity between two lists of tokens."""
    set_a, set_b = set(a), set(b)
    if not set_a and not set_b:
        return 1.0
    return len(set_a & set_b) / len(set_a | set_b)

try:
    corpus = pyconll.load_from_file(KENET_PATH)
except Exception as e:
    print(f"ERROR: Failed to read CONLLU file: {KENET_PATH}. Details: {e}", file=sys.stderr)
    sys.exit(1)

print(f"Loading corpus from '{KENET_PATH}'...")

for sentence in corpus:
    gold_tokens = [token.form for token in sentence if token.form]
    
    sentence_text = sentence.text
    
    if not sentence_text:
        print(f"WARNING: Sentence {sentence.id} has no raw text. Skipping.", file=sys.stderr)
        continue
    
    pred_tokens = tokenizer.tokenize(sentence_text, apply_lower=APPLY_LOWER)

    # Compare predictions to the gold standard
    exact_match = (gold_tokens == pred_tokens)
    missing = list(set(gold_tokens) - set(pred_tokens))
    extra = list(set(pred_tokens) - set(gold_tokens))
    acc = jaccard_similarity(gold_tokens, pred_tokens)

    rows.append({
        "sentence_id": sentence.id,
        "sentence_text": sentence_text,
        "gold_tokens": " ".join(gold_tokens),
        "pred_tokens": " ".join(pred_tokens),
        "missing_tokens": ", ".join(missing),
        "extra_tokens": ", ".join(extra),
        "exact_match": exact_match,
        "token_accuracy": round(acc, 3)
    })

if not rows:
    print("ERROR: No sentences were processed. Check the CONLLU path.", file=sys.stderr)
    sys.exit(1)

print(f"Processed {len(rows)} sentences.")

# Write the detailed analysis to a CSV file
with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)

print(f"Detailed analysis report saved to '{OUTPUT_CSV}'.")

# FINAL RESULTS
exact_count = sum(1 for r in rows if r["exact_match"])
mean_acc = sum(r["token_accuracy"] for r in rows) / len(rows)

total_sent = len(rows)
exact_ratio = exact_count / total_sent * 100

print("\n--- Structural Tokenization Performance ---")
print(f"Total Sentences: {total_sent}")
print(f"Exact Match Ratio: {exact_ratio:.2f}%")
print(f"Mean Token Accuracy (Jaccard): {mean_acc:.3f}")
