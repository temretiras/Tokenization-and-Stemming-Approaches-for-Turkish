import csv
import sys
import pandas as pd
from rule_based_tokenizer import RuleBasedTokenizer, turkish_lower

TOKENIZER_MWE_LIST_PATH = "turkish-tokenizer-rb/trmwe_list.txt" 
ABBR_LIST_PATH = "turkish-tokenizer-rb/zemberek_abbreviations.txt" 
GOLD_STANDARD_CSV_PATH = "turkish-tokenizer-rb/gold_mwe_dataset.csv"
FP_OUTPUT_CSV = "mwe_false_positives_ANALYSIS.csv"
FN_OUTPUT_CSV = "mwe_false_negatives_ANALYSIS.csv"


def calculate_metrics(tp, fp, fn):
    """Return precision, recall, and F1."""
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1_score

def evaluate_mwe_performance():
    """
    Run the tokenizer against the gold-standard MWE dataset
    and compute TP, FP, FN statistics.
    """
    
    try:
        tokenizer = RuleBasedTokenizer(
            abbreviations_path=ABBR_LIST_PATH,
            trmwe_list_path=TOKENIZER_MWE_LIST_PATH 
        )
        print("Tokenizer initialized.")
        print(f"  Abbreviation list: {ABBR_LIST_PATH} ({len(tokenizer.all_abbreviations_lower)} entries)")
        print(f"  MWE list: {TOKENIZER_MWE_LIST_PATH} ({len(tokenizer.mwe_set)} entries)\n")
    except Exception as e:
        print(f"ERROR: Tokenizer could not be initialized. Check file paths: {e}", file=sys.stderr)
        return

    total_tp, total_fp, total_fn = 0, 0, 0
    fp_analysis = []
    fn_analysis = []

    try:
        with open(GOLD_STANDARD_CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            
            for i, row in enumerate(reader):
                if len(row) < 2:
                    continue
                
                sentence_text = row[0]
                gold_merged_tokens_str = row[1]
                
                pred_tokens = tokenizer.tokenize(sentence_text, apply_lower=False)
                
                gold_tokens = gold_merged_tokens_str.split()

                pred_tokens_lower = [turkish_lower(t) for t in pred_tokens]
                gold_tokens_lower = [turkish_lower(t) for t in gold_tokens]

                pred_mwes = set(tok for tok in pred_tokens_lower if "_" in tok)
                gold_mwes = set(tok for tok in gold_tokens_lower if "_" in tok)

                tp_set = gold_mwes.intersection(pred_mwes)
                fp_set = pred_mwes.difference(gold_mwes)
                fn_set = gold_mwes.difference(pred_mwes)
                
                total_tp += len(tp_set)
                total_fp += len(fp_set)
                total_fn += len(fn_set)
                
                if fp_set:
                    fp_analysis.append({
                        "sentence_text": sentence_text,
                        "gold_tokens": " ".join(gold_tokens),
                        "pred_tokens": " ".join(pred_tokens),
                        "false_positives": ", ".join(fp_set)
                    })
                
                if fn_set:
                    fn_analysis.append({
                        "sentence_text": sentence_text,
                        "gold_tokens": " ".join(gold_tokens),
                        "pred_tokens": " ".join(pred_tokens),
                        "false_negatives": ", ".join(fn_set)
                    })

    except FileNotFoundError:
        print(f"ERROR: '{GOLD_STANDARD_CSV_PATH}' was not found.", file=sys.stderr)
        print("Ensure the generated CSV is in the same directory as this script.", file=sys.stderr)
        return
    except Exception as e:
        print(f"Evaluation failed: {e}", file=sys.stderr)
        return

    print("--- MWE Performance Evaluation ---")
    print(f"\nTotal sentences reviewed: {i + 1}")
    print("\n--- Aggregate Stats ---")
    print(f"True Positives (TP): {total_tp}")
    print(f"False Positives (FP): {total_fp}")
    print(f"False Negatives (FN): {total_fn}")
    
    precision, recall, f1_score = calculate_metrics(total_tp, total_fp, total_fn)
    
    print("\n--- MWE Scores ---")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1_score:.4f}")

    if fp_analysis:
        pd.DataFrame(fp_analysis).to_csv(FP_OUTPUT_CSV, index=False, encoding='utf-8-sig')
        print(f"\nSaved FP analysis to '{FP_OUTPUT_CSV}'.")
    
    if fn_analysis:
        pd.DataFrame(fn_analysis).to_csv(FN_OUTPUT_CSV, index=False, encoding='utf-8-sig')
        print(f"Saved FN analysis to '{FN_OUTPUT_CSV}'.")

if __name__ == "__main__":
    evaluate_mwe_performance()
